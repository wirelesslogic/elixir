import json
from flask_htmx import make_response
from flask import Blueprint, render_template, request, url_for, session

from core.decorators import htmx_view
from core.utils import string_to_list, true_false_empty

from shared import layout

from .forms import ColumnOrderForm
from .table import Table

plugin = Blueprint("table", __name__, template_folder="templates")


@plugin.route("/update-column-order/<table_name>", methods=["GET", "POST"])
@htmx_view
def update_column_order(table_name):
    form = ColumnOrderForm(request.form)

    table = Table(table_name, request)

    if form.is_submitted() and form.validate():
        received_column_data = json.loads(form.column_state.data)

        # Apply column state to table state
        temp_column_dict = {}
        for received_column in received_column_data:
            temp_column_dict[received_column["name"]] = table.state["columns"][
                received_column["name"]
            ]
            temp_column_dict[received_column["name"]]["visible"] = received_column[
                "visible"
            ]

        table.state["columns"] = temp_column_dict

        # Update the schema with visibility and order
        current_list = table.state.get("columns", None)

        if current_list is None:
            current_list = table.default_state.get("columns", {})
            table.state["columns"] = current_list

        table.prepare()

        return make_response(refresh=True)

    # Get data from config based on source
    config_data = table.default_state

    Table.apply_cache_to_dict(config_data, table.state, config_data["cache_keys"])

    return_url = url_for(request.endpoint, table_name=table_name)

    return render_template(
        "modals/column_order.jinja",
        form=form,
        submit_text="Submit",
        title="test",
        icon="cupcake",
        data=config_data,
        return_url=return_url,
        table_name=table_name,
        table_state=table.state,
        table_data=table.get_query(),
    )


@plugin.route("/update-selection/<table_name>", methods=["GET", "POST"])
@htmx_view
def update_selection(table_name):
    table = Table(table_name, request)

    if not table.default_state["selection_enabled"]:
        table.state["selection_enabled"] = table.default_state["selection_enabled"]
        return table.render_template(layout)

    select_all = table.request.get("select_all", None)
    select_individual = table.request.get("select", None)

    relevant_session = session[table.table_name]

    if select_all is not None:
        relevant_session["selection"] = {
            "override": [],
            "select_all": select_all == "True",
        }

        session.modified = True

    if select_individual is not None:
        if select_individual not in relevant_session["selection"]["override"]:
            relevant_session["selection"]["override"].append(select_individual)
        else:
            relevant_session["selection"]["override"].remove(select_individual)

        session.modified = True

    return table.render_template(layout)


@plugin.route("/update-search/<table_name>", methods=["GET", "POST"])
@htmx_view
def update_search(table_name):
    table = Table(table_name, request)

    # NOTE: needs clearer way of showing when an actual filter change is done.
    for column, props in table.state["columns"].items():
        if "search" in props:
            column_schema = table.state["schema"][column]
            search_key = f"search_{column}"

            if search_key not in table.request:
                continue

            table.reset_pagination()
            table.reset_selection()
            table.state["temp"]["input_autofocus"] = column

            search_values = table.request.getlist(search_key)
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

    return table.render_template(layout)


@plugin.route("/reset-search/<table_name>", methods=["GET", "POST"])
@htmx_view
def reset_search(table_name):
    table = Table(table_name, request)

    # Reset search
    table.reset_search()
    table.reset_pagination()
    table.reset_selection()

    return table.render_template(layout)


@plugin.route("/update-sort/<table_name>", methods=["GET", "POST"])
@htmx_view
def update_sort(table_name):
    table = Table(table_name, request)

    sort_by = table.request.get("sort_by", None)
    sort_dir = table.request.get("sort_dir", None)

    if sort_by:
        for column, props in table.state["columns"].items():
            if "sort" in props:
                props["sort"] = "not"

        if sort_by in table.state["columns"]:
            table.state["columns"][sort_by]["sort"] = sort_dir

    return table.render_template(layout)


@plugin.route("/change-page/<table_name>", methods=["GET", "POST"])
@htmx_view
def change_page(table_name):
    table = Table(table_name, request)

    page = table.request.get(
        "page", table.state["pagination"]["current_page"], type=int
    )

    table.state["pagination"]["current_page"] = page

    return table.render_template(layout)


@plugin.route("/change-items-per-page/<table_name>", methods=["GET", "POST"])
@htmx_view
def change_items_per_page(table_name):
    table = Table(table_name, request)

    items_per_page = table.request.get(
        "items_per_page", table.state["pagination"]["items_per_page"], type=int
    )

    table.state["pagination"]["items_per_page"] = items_per_page

    table.reset_pagination()

    return table.render_template(layout)
