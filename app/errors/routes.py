from flask import render_template, current_app

from app import db
from . import bp

# Register as app-wide handlers via the blueprint
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404 

@bp.app_errorhandler(500)
def internal_error(error):
    # Log the full stack trace to app logger (goes to SMTP handler)
    current_app.logger.exception("Unhandled exception")
    db.session.rollback()
    return render_template("500.html"), 500
