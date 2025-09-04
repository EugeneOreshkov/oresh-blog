from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import render_template, redirect, flash, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from . import bp

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST" and not form.validate():
        current_app.logger.warning('Registration form failed to validate: %r', form.errors)
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            phone = form.phone.data,
        )
        current_app.logger.info(
            "Registering new user: username=%s, email=%s, phone=%s",
            user.username, user.email, user.phone
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thank you for registering. You can now log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form, current_route=request.endpoint)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        stmt = sa.select(User).where(User.username == form.username.data)
        user = db.session.scalars(stmt).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        flash("Login requested successfully.")
        return redirect(next_page)
    return render_template('login.html', title = 'Sign in', form=form, current_route=request.endpoint)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
