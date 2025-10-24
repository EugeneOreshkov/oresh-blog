from flask import Blueprint

bp = Blueprint("reset_password", __name__, template_folder="templates")

from app.post import routes # noqa: F401,E402