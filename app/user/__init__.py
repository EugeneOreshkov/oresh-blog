from flask import Blueprint

bp = Blueprint("users", __name__, template_folder="templates")

from app.user import follow # noqa: F401,E402
