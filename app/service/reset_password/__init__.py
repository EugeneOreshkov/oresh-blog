from flask import Blueprint

bp = Blueprint("reset_password", __name__, template_folder="templates")

from app.service.reset_password import routes, password_reset_service # noqa: F401,E402