from flask import Blueprint

bp = Blueprint("avatars", __name__, template_folder="templates")

from app.avatar import avatar_stock  # noqa: F401,E402
