from flask import render_template
from flask_login import login_required

from app.models import Post

from . import bp

@bp.route("/search")
@login_required
def search():
    posts = Post.get_all_posts()
    return render_template("search.html", title="Найти", posts=posts)