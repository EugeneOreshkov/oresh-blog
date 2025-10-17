from flask import Blueprint

bp = Blueprint("posts", __name__, template_folder="templates")

from app.post import routes # noqa: F401,E402