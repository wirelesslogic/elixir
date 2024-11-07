Module plugins.table.table
==========================

Functions
---------

    
`true_false_empty(input_item: str)`
:   

Classes
-------

`Table(model, table_name, default_state, request)`
:   Initialize the Table with state management.
    
    Parameters:
    - model (peewee.Model): The model to use for the table.
    - table_name (str): The name of the table.
    - default_state (dict): The default state configuration for the table.
    - request (flask.request): The request object.

    ### Class variables

    `clear_cache`
    :

    `clear_session`
    :

    ### Static methods

    `apply_cache_to_dict(input_dict, cache_data, target_keys)`
    :

    ### Methods

    `apply_cache_to_state(self, cache_data, target_keys)`
    :

    `apply_pagination(self, query: peewee.ModelSelect)`
    :   Apply pagination to the query based on the table's state.
        
        Uses the 'start' and 'end' values from the table state's pagination data.

    `apply_schema(self, default_state)`
    :

    `apply_search(self, query: peewee.ModelSelect)`
    :   Apply search terms to the query based on the table's state.

    `apply_sorting(self, query: peewee.ModelSelect)`
    :   Apply sorting to the query based on the table's state.
        
        Uses the 'sort_column' and 'sort_dir' values from the table state.

    `build_cache_dict(self, source)`
    :

    `build_default_cache_dict(self)`
    :

    `clear_temp_values(self)`
    :

    `get_cached_values(self)`
    :   Retrieve the state of a table from the cache.

    `get_enum_class_for_column(self, column_name: str)`
    :   Get the enum class for a given column from the Peewee model.

    `get_query(self)`
    :

    `get_unique_values_for_column(self, column_name)`
    :   Get unique values for a column from the database, excluding null, empty, or single space values.

    `get_visible_fields(self)`
    :   Get the visible fields from the table's state.

    `initialize_cache(self)`
    :

    `initialize_session(self)`
    :

    `modify_query(self, query)`
    :   Modify the provided query using the table's state.
        
        This function applies pagination, sorting, and searching to the query.

    `render_htmx(self, query: peewee.ModelSelect)`
    :

    `render_template(self, layout: core.layout.Layout, query_override: peewee.ModelSelect = None)`
    :

    `reset_pagination(self)`
    :

    `reset_search(self)`
    :

    `reset_selection(self)`
    :

    `set_pagination_base(self)`
    :

    `set_pagination_full(self, total_items=0)`
    :

    `set_search_and_sorting(self)`
    :

    `set_selection(self)`
    :

    `set_table_state(self)`
    :   Set the state of a table in the cache.

    `set_visibility_and_order(self)`
    :

    `update_schema_visibility_and_order(self)`
    :

    `update_schema_with_model_field_types(self, state)`
    :