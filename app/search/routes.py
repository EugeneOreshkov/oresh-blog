from flask import render_template
from flask_login import login_required

from . import bp

@bp.route("/search")
@login_required
def search():
    return render_template("search.html", title="Найти")