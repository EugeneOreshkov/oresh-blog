from flask import render_template
from app import app
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
@app.route('/about')
def about():
    return render_template('about.html')