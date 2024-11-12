from easydict import EasyDict as edict
from copy import deepcopy
from jinja2 import TemplateNotFound
from flask_login import current_user
from flask_htmx import make_response
from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    abort,
)

from elixir.core.cache import cache
from elixir.core.config import cfg
from elixir.core.decorators import htmx_view
from elixir.core.htmx import htmx
from elixir.core.logger import log

from elixir.plugins.table import Table

from .forms import PlaceholderForm

plugin = Blueprint("modals", __name__, template_folder="templates")


@plugin.route("/table-modal")
def table_modal():
    if not htmx:
        abort(404)

    template = find_template(request.args.get("template", "partials/void.jinja"))

    source = request.args.get("source", None)
    config_target = source.split(".", 1)[0]

    # Get data from config based on source
    data = edict(deepcopy(cfg[config_target].table))

    cache_data = hit_cache(
        cache.get_key("table", source, user_uuid=current_user.uuid), source
    )

    Table.apply_cache_to_dict(data, cache_data["table"], data["cache_keys"])

    target = request.args.get("target", "this")

    return handle_template(template, source, target, data, request)


@plugin.route("/placeholder-modal")
@htmx_view
def modal():
    form = PlaceholderForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            return make_response(refresh=True)

    return render_template(
        "placeholders/modal.jinja",
        form=form,
        action=f"edit/{id}",
        submit_text="Submit",
        title="test",
        icon="cupcake",
    )


def find_template(template):
    if template == "partials/void.jinja":
        return template

    try:
        current_app.jinja_env.get_template(template)
    except TemplateNotFound:
        template = "partials/modals/notfound.jinja"

    return template


def handle_template(template, source, target, data, input_request):
    return render_template(
        "partials/modal.jinja",
        template=template,
        source=source,
        target=target,
        data=data,
        size=input_request.args.get("size", "default"),
        title=input_request.args.get("title", "Placeholder Title"),
        icon=input_request.args.get("icon", "cupcake"),
        submit_text=input_request.args.get("button", "Apply"),
    )


def hit_cache(cache_key, source):
    cache_data = cache.get_data(cache_key)

    if cache_data is None:
        return cfg.get(source.split(".")[0], None)

    return {"table": cache_data}
