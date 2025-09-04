from datetime import datetime

import sqlalchemy as sa
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required

from app import app, db
from app.profile.forms import EditProfileForm
from app.models import User
from . import bp

@bp.route('/user/<username>')
@login_required
def user(username):
    stmt = sa.select(User).where(User.username == username)
    user = db.first_or_404(stmt)
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('profile.html', title='User', user=user, posts=posts, current_route=request.endpoint)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
    return render_template('edit_profile.html', title='Edit Profile', form=form, current_route=request.endpoint)

@bp.before_request
def before_request():
    # update last_login timestamp for logged-in users (shown in profile column)
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        db.session.commit()
