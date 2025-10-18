from flask import render_template, request
from flask_login import current_user, login_required

from app.service.greeting_message import GreetingMessage
from app import app, db

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Main page."""    
    greeting = GreetingMessage.get_greeting()
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(
        current_user.following_posts(),
        page = page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    return render_template(
        'index.html',
        title='Brainy',
        posts=posts.items,        
        greeting=greeting
    )

@app.route('/about')
def about():
    return render_template('about.html', title='О нас')