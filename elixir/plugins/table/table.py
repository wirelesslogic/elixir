from typing import List
from copy import deepcopy
from easydict import EasyDict
from flask import session
from flask import render_template
from flask_login import current_user
from peewee import (
    BigIntegerField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    BooleanField,
    IntegerField,
    ModelSelect,
    SmallIntegerField,
)

from core.htmx import htmx
from core import log
from config import cfg
from core.utils import string_to_list, true_false_empty
from core.layout import Layout

from db.custom_fields import EnumField

from shared import cache, models


class Table:
    clear_cache = False
    clear_session = False

    def __init__(self, table_name, request):
        """
        Initialize the Table with state management.

        Parameters:
        - model (peewee.Model): The model to use for the table.
        - table_name (str): The name of the table.
        - default_state (dict): The default state configuration for the table.
        - request (flask.request): The request object.
        """
        self.table_name = table_name
        split_name = self.table_name.split(".")

        self.default_state = cfg[split_name[0]][f"{split_name[1]}_table"]
        self.model = models.get_model(self.default_state.model)
        self.request = request.values

        for key, value in cfg.table.defaults.items():
            self.default_state[f"default_{key}"] = value

        self.state = self.apply_schema(self.default_state)

        self.initialize_session()
        self.initialize_cache()
        self.clear_temp_values()

    def prepare(self):
        self.apply_session_items()
        self.set_table_state()
        self.set_activity()

    def set_activity(self):
        select_all = self.state.selection["select_all"]
        search_state = self.strip_search_from_columns()

        has_search = False

        for key, item in search_state.items():
            if len(item) > 0:
                has_search = True

        has_selection = False

        if len(self.state.selection["override"]) > 0:
            has_selection = True

        has_any_selection_values = select_all or has_selection
        exclude_select_all_without_search = not select_all or has_search

        self.state.disable_bulk_actions = not (
            has_any_selection_values and exclude_select_all_without_search
        )

    def strip_search_from_columns(self):
        temp_dict = {}

        for column, props in self.state.columns.items():
            if "search" in props:
                temp_dict[column] = props["search"]

        return temp_dict

    def initialize_session(self):
        if session.get(self.table_name, None) is None:
            session[self.table_name] = {}

        if (
            session[self.table_name].get("selection", None) is None
            or self.clear_session
        ):
            session[self.table_name]["selection"] = self.default_state["selection"]
            session.modified = True

    def apply_schema(self, default_state):
        state = EasyDict(deepcopy(default_state))
        # Update the schema with the model field types
        self.update_schema_with_model_field_types(state)

        for column, props in state["schema"].items():
            # Ensure settings exists under style, if style exists
            if "style" in props and "settings" not in props["style"]:
                props["style"]["settings"] = {}

            # Update the unique values for the select fields only if they are not present
            # If it's a select type and options list is empty
            if (
                "search" in props
                and props["search"]["type"] == "select"
                and not props["search"]["options"]
            ):
                if props["data_type"] != "enum":
                    state["columns"][column]["options"] = (
                        self.get_unique_values_for_column(column)
                    )
                    continue

                enum_cls = self.get_enum_class_for_column(column)

                if enum_cls:
                    # Get all possible values for the enum
                    state["columns"][column]["options"] = [
                        item.name.capitalize() for item in enum_cls
                    ]

        return state

    def initialize_cache(self):
        cache_data = self.get_cached_values()
        self.apply_cache_to_state(cache_data, self.default_state["cache_keys"])

    def apply_cache_to_state(self, cache_data, target_keys):
        Table.apply_cache_to_dict(self.state, cache_data, target_keys)

    @staticmethod
    def apply_cache_to_dict(input_dict, cache_data, target_keys):
        for key in target_keys:
            if cache_data.get(key):
                input_dict[key] = cache_data[key]

    def build_default_cache_dict(self):
        return self.build_cache_dict(self.state)

    def build_cache_dict(self, source):
        cache_dict = {}

        for key in self.default_state["cache_keys"]:
            cache_dict[key] = source[key]

        return cache_dict

    def get_cached_values(self):
        """Retrieve the state of a table from the cache."""
        cache_key = cache.get_key("table", self.table_name, user_uuid=current_user.uuid)

        if self.clear_cache:
            log.debug("Clearing Table cache")
            cache.delete(cache_key)

        return cache.get_or_set(cache_key, self.build_default_cache_dict)

    def set_table_state(self):
        """Set the state of a table in the cache."""
        cache_key = cache.get_key("table", self.table_name, user_uuid=current_user.uuid)
        cache_data = self.build_cache_dict(self.state)
        cache.set_data(cache_key, cache_data)

    def apply_session_items(self):
        if self.default_state["selection_enabled"]:
            self.state["selection"] = session[self.table_name]["selection"]

    def clear_temp_values(self):
        self.state["temp"] = {"temp": {"input_autofocus": ""}}

    def update_schema_with_model_field_types(self, state):
        # Define a mapping of field types to the corresponding string values
        type_mapping = {
            CharField: "text",
            EnumField: "enum",
            IntegerField: "number",
            SmallIntegerField: "number",
            BigIntegerField: "number",
            DecimalField: "decimal",
            DateField: "date",
            DateTimeField: "datetime",
            BooleanField: "bool",
        }

        # Loop through the model fields and update the schema.
        for field_name, field_obj in self.model._meta.fields.items():
            field_type = type_mapping.get(type(field_obj))

            if field_type and field_name in state["schema"]:
                state["schema"][field_name]["data_type"] = field_type

    def set_search_and_sorting(self):
        # Sorting
        sort_by = self.request.get("sort_by", None)
        sort_dir = self.request.get("sort_dir", None)

        if sort_by:
            for column, props in self.state["columns"].items():
                if "sort" in props:
                    props["sort"] = "not"

            if sort_by in self.state["columns"]:
                self.state["columns"][sort_by]["sort"] = sort_dir

        # Searching
        # Reset search
        search = self.request.get("search", None)
        if search is not None and search == "reset":
            self.reset_search()
            self.reset_pagination()
            self.reset_selection()

            return

        # NOTE: needs clearer way of showing when an actual filter change is done.
        # Update search
        for column, props in self.state["columns"].items():
            if "search" in props:
                column_schema = self.state["schema"][column]
                search_key = f"search_{column}"

                if search_key not in self.request:
                    continue

                self.reset_pagination()
                self.reset_selection()
                self.state["temp"]["input_autofocus"] = column

                search_values = self.request.getlist(search_key)
                search_type = column_schema["search"]["type"]

                match search_type:
                    case "select":
                        props["search"] = search_values if search_values != [""] else []
                    case "bulk":
                        props["search"] = (
                            string_to_list(search_values[0])
                            if search_values != [""]
                            else []
                        )
                    case "bool":
                        props["search"] = true_false_empty(
                            search_values[0] if search_values else ""
                        )
                    case _:
                        props["search"] = search_values[0] if search_values else ""

    def set_pagination_full(self, total_items=0):
        page = self.state["pagination"]["current_page"]
        items_per_page = self.state["pagination"]["items_per_page"]
        total_pages = (total_items + items_per_page - 1) // items_per_page
        page = max(1, min(page, total_pages))

        self.state["pagination"].update(
            {
                "current_page": page,
                "total_items": total_items,
                "total_pages": total_pages,
                "items_per_page": items_per_page,
                "start": ((page - 1) * items_per_page) + 1,
                "end": min(page * items_per_page, total_items),
            }
        )

    def get_enum_class_for_column(self, column_name: str):
        """Get the enum class for a given column from the Peewee model."""
        field = getattr(self.model, column_name, None)
        if isinstance(field, EnumField):
            return field.choices
        return None

    def get_visible_fields(self):
        """Get the visible fields from the table's state."""
        visible_fields = [
            field
            for field, props in self.state["columns"].items()
            if props.get("visible") and props["visible"] is True
        ] + [self.state["identifier_column"]]

        return [getattr(self.model, field) for field in visible_fields]

    def modify_query(self, query):
        """
        Modify the provided query using the table's state.

        This function applies pagination, sorting, and searching to the query.
        """
        query = self.apply_search(query)

        total_items = query.count()
        self.set_pagination_full(total_items)

        query = self.apply_pagination(query)
        query = self.apply_sorting(query)

        return query

    def apply_pagination(self, query: ModelSelect):
        """
        Apply pagination to the query based on the table's state.

        Uses the 'start' and 'end' values from the table state's pagination data.
        """
        start = self.state["pagination"]["start"] - 1
        end = self.state["pagination"]["end"]

        return query.offset(start).limit(end - start)

    def apply_sorting(self, query: ModelSelect):
        """
        Apply sorting to the query based on the table's state.

        Uses the 'sort_column' and 'sort_dir' values from the table state.
        """
        sort_column, sort_dir = None, None
        for column, props in self.state["columns"].items():
            if "sort" in props and props["sort"] != "not":
                sort_column = column
                sort_dir = props["sort"]

        if sort_column and sort_dir:
            column_attr = getattr(self.model, sort_column)
            if sort_dir == "asc":
                return query.order_by(column_attr)
            else:
                return query.order_by(column_attr.desc())
        return query

    def apply_search(self, query: ModelSelect):
        """
        Apply search terms to the query based on the table's state.
        """
        search_terms = {}

        for column, props in self.state["columns"].items():
            if (
                "search" in props
                and "visible" in props
                and props["visible"]
                and props["search"] is not None
                and props["search"] != ""
                and props["search"] != []
            ):
                search_terms[column] = props["search"]

        def handle_enum(column_attr, value):
            enum_cls = self.get_enum_class_for_column(column_attr.name)

            if isinstance(value, list):
                return [enum_cls.from_str(val) if val else None for val in value]

            return enum_cls.from_str(value) if value else None

        handlers = {
            "text": lambda attr, value: attr.contains(value),
            "number": lambda attr, value: attr.contains(value),
            "bool": lambda attr, value: attr == value,
            # "number": lambda attr, value: attr == int(value),
            "enum": lambda attr, value: attr == handle_enum(attr, value),
            "date": lambda attr, value: attr.cast(CharField.field_type).like(
                value + "%"
            ),
            "datetime": lambda attr, value: attr.cast(CharField.field_type).like(
                value + "%"
            ),
        }

        for column, search_value in search_terms.items():
            column_attr = getattr(self.model, column)
            column_type = (
                self.state["schema"].get(column, {}).get("data_type", "text")
            )  # Default to "text"
            handler = handlers.get(column_type)

            if not handler:
                continue

            # Check if the search_value is a list or single value
            if isinstance(search_value, list):
                conditions = [handler(column_attr, value) for value in search_value]
                combined_condition = conditions[0]

                for condition in conditions[1:]:
                    combined_condition |= condition

                query = query.where(combined_condition)
            else:
                condition = handler(column_attr, search_value)
                query = query.where(condition)

        return query

    def get_unique_values_for_column(self, column_name):
        """Get unique values for a column from the database, excluding null, empty, or single space values."""
        column_attr = getattr(self.model, column_name)

        # Exclude null, empty string and single space values
        query = (
            self.model.select(column_attr)
            .where(
                column_attr.is_null(False) & (column_attr != "") & (column_attr != " ")
            )
            .distinct()
            .order_by(column_attr)
        )

        values = [item.get(column_name) for item in query.dicts()]

        # Further ensure that there are no empty, null, or single space values in the list
        return [value for value in values if value not in (None, "", " ")]

    def reset_search(self):
        for column, props in self.state["columns"].items():
            if "search" in props:
                props["search"] = self.default_state["columns"][column]["search"]

    def reset_pagination(self):
        self.state["pagination"]["current_page"] = 1

    def reset_selection(self):
        session[self.table_name]["selection"] = self.default_state["selection"]
        session.modified = True

        self.state["selection"] = self.default_state["selection"]

    def get_query(self):
        temp_query = self.model.select(*self.get_visible_fields())

        return self.modify_query(temp_query)

    def render_template(self, layout: Layout, query_override: ModelSelect = None):
        self.prepare()

        query = query_override

        if query is None:
            query = self.get_query()

        if htmx:
            return self.render_htmx(query)

        return layout.render_template(
            "sections/table_skeleton.jinja",
            table_name=self.table_name,
            table_state=self.state,
            table_data=query,
        )

    def render_htmx(self, query: ModelSelect):
        partials = {"default": "partials/table.jinja"}

        render_type = self.request.get("render", None)

        template_file = partials["default"]

        if render_type is not None and render_type in partials:
            template_file = partials[render_type]

        return render_template(
            template_name_or_list=template_file,
            table_name=self.table_name,
            table_state=self.state,
            table_data=query,
        )
