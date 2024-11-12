import random

from elixir.core.cache import cache
from elixir.core.config import cfg
from elixir.core.logger import log
from elixir.core.utils import is_valid_next_route
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import LoginManager, current_user, login_user, logout_user
from elixir.plugins.auth.otp import OTPService
from elixir.plugins.auth.rate_limiter import rate_limiter

from .forms import LoginForm, OTPForm
from .models import User

plugin = Blueprint("auth", __name__, template_folder="templates")

login_manager = LoginManager()

# These endpoints are not included in basic auth checks
public_endpoints = {
    "auth.login",
    "auth.forgot_password",
    "auth.verify_otp",
    "static",
    "static_from_root",
}


def skip_basic_auth(namespace):
    def decorator(func):
        public_endpoints.add(f"{namespace}.{func.__name__}")
        log.info(
            f"Endpoint BASIC authentication skip registered as public: {namespace}.{func.__name__}"
        )

        return func

    return decorator


@plugin.before_app_request
def default_login_required():
    if request.endpoint in public_endpoints or current_user.is_authenticated:
        return

    return current_app.login_manager.unauthorized()


@plugin.record_once
def on_load(state):
    login_manager.init_app(state.app)


@plugin.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_or_none(User.email == form.email.data)

        if user and rate_limiter.is_allowed_attempt(user.email):
            if user.verify_password(form.password.data):
                remember_me = request.form.get("remember_me", False)
                next_route = request.args.get("next")
                if not is_valid_next_route(next_route):
                    next_route = url_for("main.index")

                # TODO Make sure sessions are indeed per user
                # as we've seen some weird behavior with sessions
                if user.is_otp_enabled:
                    session["user_id"] = user.id
                    session["remember_me"] = remember_me
                    session["next_route"] = next_route
                    return redirect(url_for("auth.verify_otp"))
                else:
                    login_user(user, remember=remember_me)
                    return redirect(next_route)
            else:
                rate_limiter.record_failed_attempt(user.email)
                flash("Invalid username or password.", "error")
        else:
            flash("Too many failed attempts. Please try again later.", "error")

    theme, login_text = get_theme_and_text("login")
    return render_template(
        "login.jinja",
        form=form,
        theme=theme,
        login_text=login_text,
    )


@plugin.route("/login/two_factor_auth", methods=["POST", "GET"])
def verify_otp():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    form = OTPForm()

    if form.validate_on_submit():
        user_id = session.get("user_id")
        remember_me = session.get("remember_me", False)
        next_route = session.get("next_route", url_for("main.index"))

        user = User.get_or_none(User.id == user_id)

        if user and rate_limiter.is_allowed_attempt(user.email):
            otp_service = OTPService(user)
            if otp_service.verify_otp(form.auth_code.data):
                session.clear()
                login_user(user, remember=remember_me)
                return redirect(next_route)
            else:
                rate_limiter.record_failed_attempt(user.email)
                flash("Invalid authentication code.", "error")
        else:
            session.clear()
            flash("Too many failed attempts. Please try again later.", "error")
            return redirect(url_for("auth.login"))

    theme, _ = get_theme_and_text()
    return render_template(
        "otp.jinja",
        form=form,
        theme=theme,
        login_text="Verify",
    )


@plugin.route("/logout")
def logout():
    cache.invalidate(cache.get_key(user_uuid=current_user.uuid))
    session.clear()
    logout_user()
    return redirect(url_for("auth.login"))


@plugin.route("/forgot-password")
def forgot_password():
    theme, forgot_text = get_theme_and_text("forgot_password")
    return render_template(
        "forgot_password.jinja",
        theme=theme,
        forgot_text=forgot_text,
    )


@login_manager.user_loader
def load_user(user_uuid):
    if user_uuid is None:
        return None

    def retrieve_and_serialize_user():
        user = User.get_or_none(User.uuid == user_uuid)
        return user.serialize() if user else None

    user_data = cache.get_or_set(
        cache.get_key(user_uuid=user_uuid),
        retrieve_and_serialize_user,
    )

    return User.deserialize(user_data) if user_data else None


@login_manager.unauthorized_handler
def unauthorized():
    session["next"] = request.endpoint
    return redirect(url_for("auth.login"))


def get_theme_and_text(category="login"):
    themes = [
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

    texts = {
        "login": [
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
            "CLICK ME!! DO IT!!",
        ],
        "forgot_password": [
            "This makes me sad.",
            "Oh no, not again.",
            "C'est la vie.",
            "Why do we forget? Why?!",
            "Bummer.",
            "Oh dear.",
        ],
    }

    return random.choice(themes), random.choice(texts[category])
