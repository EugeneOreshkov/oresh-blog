from flask import Blueprint

bp = Blueprint("auth", __name__, template_folder="templates")

from app.auth import authentication # noqa: F401,E402