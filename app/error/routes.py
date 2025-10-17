from flask import render_template, current_app

from app import db, messages
from . import bp

# Register as app-wide handlers via the blueprint

@bp.app_errorhandler(404)
def not_found_error(_error):
    return render_template("404.html", error=messages.ERROR_404_MESSAGE), 404 

@bp.app_errorhandler(500)
def internal_error(error):
    # Log the full stack trace to app logger (goes to SMTP handler)
    current_app.logger.exception(f"Unhandled exception {error}")
    db.session.rollback()
    return render_template("500.html", error=messages.ERROR_500_MESSAGE), 500
