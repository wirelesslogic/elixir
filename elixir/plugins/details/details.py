from flask import render_template
from peewee import (
    ModelSelect,
)

from core.htmx import htmx
from config import cfg
from core.layout import Layout
from core import log

from shared import models


class Details:
    query_overrides = {}

    def __init__(self, detail_page_name, page, request, main_id):
        self.request = request
        self.main_id = main_id
        self.page = page

        details_split_name = detail_page_name.split(".")

        self.route_info = {
            "full": detail_page_name,
            "base": details_split_name[0],
            "name": details_split_name[1],
        }

        self.menu = cfg[self.route_info["base"]]["details"]["menu"]
        self.config = cfg[self.route_info["base"]]["details"]["pages"][page]
        self.model = models.get_model(self.config.model)

    def prepare(self):
        pass

    def load_query_overrides(self, query_overrides):
        self.query_overrides = query_overrides

    def get_base_query(self):
        return self.model.select().where(self.config.identifier_column == self.main_id)

    def render_template(self, layout: Layout):
        self.prepare()

        base_query = self.get_base_query()
        query_override = self.query_overrides.get(self.page, None)

        query = (
            base_query
            if query_override is None
            else query_override(
                base_query,
                self.model,
                self.main_id,
                self.config.identifier_column,
            )
        )

        if htmx:
            return self.render_htmx(query)

        return layout.render_template(
            "sections/detail_skeleton.jinja",
            detail_route_info=self.route_info,
            detail_id=self.main_id,
            detail_config=self.config,
            detail_menu=self.menu,
            detail_data=query,
        )

    def render_htmx(self, query: ModelSelect):
        partials = {"default": "base.jinja"}

        render_type = self.request.get("render", None)

        template_file = partials["default"]

        if render_type is not None and render_type in partials:
            template_file = partials[render_type]

        return render_template(
            template_name_or_list=template_file,
            detail_route_info=self.route_info,
            detail_id=self.main_id,
            detail_config=self.config,
            detail_menu=self.menu,
            detail_data=query,
        )
