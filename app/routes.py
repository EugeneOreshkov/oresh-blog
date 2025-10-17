from datetime import datetime

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import app, db
from app.post.forms import PostForm
from app.models import Post

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Main page."""    
    # Greeting message
    hour = datetime.now().hour
    periods = [(range(5,12), 'Доброе утро☀️'),
               (range(12,18), 'Добрый день🌤️'),
               (range(18,24), 'Добрый вечер🌙'),
               (range(0,5), 'Добрый вечер🌙'),]
    greeting = "Привет"
    for period, greeting_text in periods:
        if hour in period:
            greeting = greeting_text
            break
    
    posts = Post.get_all_posts()

    return render_template(
        'index.html',
        title='Oreshkov',
        posts=posts,        
        greeting=greeting
    )

@app.route('/about')
def about():
    return render_template('about.html', title='About')