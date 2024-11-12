import random

from elixir.core.config import cfg
from elixir.core.logger import log
from elixir.core.utils import is_valid_next_route
from flask import Blueprint, redirect, render_template, request, session, url_for

from .forms import LoginForm

plugin = Blueprint("guard", __name__, template_folder="templates")


@plugin.before_app_request
def default_login_required():
    # These endpoints are publicly available for everyone
    public_endpoints = set(
        [
            "guard.login",
            "static",
            "static_from_root",
        ]
    )

    if "access_granted" not in session and not request.endpoint in public_endpoints:
        return redirect(url_for("guard.login"))


@plugin.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        if form.password.data != cfg.plugins.guard.password:
            return redirect(url_for("guard.login"))

        session["access_granted"] = True

        next_route = request.args.get("next")

        if not is_valid_next_route(next_route):
            next_route = "main.index"

        return redirect(url_for(next_route))

    next_route = request.args.get("next")
    if not is_valid_next_route(next_route):
        next_route = url_for("main.index")

    theme = [
        "blue-theme",
        "green-theme",
        "purple-theme",
        "red-theme",
        "yellow-theme",
        "orange-theme",
        "pink-theme",
        "turquoise-theme",
        "indigo-theme",
    ]

    funny_login_texts = [
        "Beam Me Up!",
        "Let's Dive In!",
        "Jump In, the Water's Fine!",
        "Open Sesame!",
        "Unleash the Magic",
        "Engage! 🚀",
        "Onward and Inward!",
        "Summon the Portal",
        "Let the Adventure Begin!",
        "Press to Impress",
        "Tap if You Dare",
        "Login & Liftoff!",
        "Enter the Dragon",
        "Knock Knock! Who's there?",
        "Into the Rabbit Hole",
        "Let's Roll!",
        "Bring on the Fun",
        "Unveil the Secrets",
        "One Small Tap for Man...",
        "To Infinity & Beyond!",
    ]

    return render_template(
        "guard/login.jinja",
        form=form,
        next=next_route,
        theme=random.choice(theme),
        login_text=random.choice(funny_login_texts),
    )


@plugin.route("/logout")
def logout():
    session.pop("access_granted", None)
    return redirect(url_for("guard.login"))
