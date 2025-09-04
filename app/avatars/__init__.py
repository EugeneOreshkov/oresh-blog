from flask import Blueprint

bp = Blueprint("avatars", __name__, template_folder="templates")

from app.avatars import avatar_stock  # noqa: F401,E402
