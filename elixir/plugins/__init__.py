from core.blueprint_loader import load_blueprint


def load_plugins(app, input_plugins):
    if input_plugins is None:
        return

    for plugin in input_plugins:
        library = f"plugins.{plugin}"
        blueprint_key = "plugin"

        load_blueprint(app, library, blueprint_key)
