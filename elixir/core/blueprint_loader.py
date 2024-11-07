import importlib

from .logger import log


def load_blueprint(flask_app, library, blueprint_key):
    try:
        log.debug(f'loading {library}')

        library_init = importlib.import_module(library)
        library_routes = importlib.import_module(f"{library}.routes")

        component_prefix = getattr(
            library_routes,
            blueprint_key,
        )

        route_prefix = getattr(
            library_init,
            "ROUTE_PREFIX",
            None,
        )

        if route_prefix is None:
            log.warn(f"Missing ROUTE_PREFIX attribute for {library}. Defaulting to: \"\"")
            route_prefix = ""

        flask_app.register_blueprint(component_prefix, url_prefix=route_prefix)
    except ModuleNotFoundError as e:
        log.exception(f"{library} could not be found.")