from flask import render_template
from app import app
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Oreshkov'}
    return render_template('index.html', title = 'Oreshkov', user=user)