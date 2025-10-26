from flask import abort, logging, render_template, request, url_for
from flask_login import login_required

from app.service.greeting_message import get_greeting
from app.service.pagination import get_following_posts_with_pagination
from app import app

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Main page."""     
    greeting = get_greeting()
    page = request.args.get('page', 1, type=int)
    posts = get_following_posts_with_pagination(page)

    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    
    return render_template(
        'index.html',
        title='Brainy',
        posts=posts.items,        
        greeting=greeting,
        next_url=next_url,
        prev_url=prev_url
    )

@app.route('/about')
def about():
    return render_template('about.html', title='О нас')