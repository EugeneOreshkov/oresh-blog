from flask import render_template, redirect, flash, url_for
from app import app
from app.forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Oreshkov'}
    posts = [
        {
        'author' : {'username': 'Oreshkov'},
        'body' : 'How I marathoned 120 days of Python'
        },
        {
            'author': {'username': 'Jennie'},
            'body': 'A brief introduction to Flask'
        }
    ]
    return render_template('index.html', title = 'Oreshkov', user=user, posts=posts)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested successfully")
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Sign in', form=form)
@app.route('/about')
def about():
    return render_template('about.html', title='About')
