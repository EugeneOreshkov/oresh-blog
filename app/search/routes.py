from flask import render_template, request, url_for
from flask_login import login_required

from app.service.pagination import get_all_posts_with_pagination

from . import bp

@bp.route("/search")
@login_required
def search():    
    page = request.args.get('page', 1, type=int)
    posts = get_all_posts_with_pagination(page)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template(
        'search.html',
        title='Найти',
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url     
    )
    