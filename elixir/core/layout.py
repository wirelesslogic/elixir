from flask import render_template, request
from easydict import EasyDict

from elixir.core.config import cfg


class Layout:
    menu: EasyDict = EasyDict({})

    def augment_menu(self, menu_dict, current_route):
        augmented_menu = {}
        active_name = None

        for key, item in menu_dict.items():
            augmented_item = item.copy()  # Shallow copy the current menu item
            item_route = item.get("route")
            item_submenu = item.get("submenu")

            is_active = item_route == current_route

            if item_submenu:
                augmented_submenu, submenu_name = self.augment_menu(
                    item_submenu, current_route
                )
                augmented_item["submenu"] = augmented_submenu
                is_active = is_active or any(
                    subitem.get("has_active_route")
                    for subitem in augmented_submenu.values()
                )
                if submenu_name:
                    active_name = submenu_name

            if is_active and not active_name:
                active_name = item.get("name")

            augmented_item["has_active_route"] = is_active
            augmented_menu[key] = augmented_item

        return augmented_menu, active_name

    def render_template(self, template_name, title=None, **kwargs):
        augmented_menu, active_name = self.augment_menu(self.menu, request.endpoint)

        if title:
            active_name = title

        return render_template(
            template_name,
            title=active_name,
            menu_items=augmented_menu,
            layout=self,
            **kwargs,
        )

layout: Layout = Layout()
layout.menu = cfg.menu
