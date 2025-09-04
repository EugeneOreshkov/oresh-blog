import sqlalchemy as sa
from flask import render_template, request
from flask_login import login_required

from app import app, db
from app.models import Post

@app.route('/')
@app.route('/index')
@login_required
def index():
    stmt = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.session.scalars(stmt).all()
    return render_template('index.html', title='Oreshkov', posts=posts, current_route=request.endpoint)

@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='About')