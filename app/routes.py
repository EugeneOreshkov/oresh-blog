from flask import render_template
from flask_login import login_required

from app.service.greeting_message import GreetingMessage
from app import app
from app.models import Post

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Main page."""    
    greeting = GreetingMessage.get_greeting()
    posts = Post.get_all_posts()

    return render_template(
        'index.html',
        title='Brainy',
        posts=posts,        
        greeting=greeting
    )

@app.route('/about')
def about():
    return render_template('about.html', title='О нас')