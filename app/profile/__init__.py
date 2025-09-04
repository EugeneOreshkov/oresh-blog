from flask import Blueprint

bp = Blueprint("profile", __name__, template_folder="templates")

from app.profile import user_profile # noqa: F401,E402
