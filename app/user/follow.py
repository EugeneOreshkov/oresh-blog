import sqlalchemy as sa
from flask import app, flash, redirect, url_for
from flask_login import current_user, login_required

from app.models import User
from app.user.forms import EmptyForm
from app import db
from . import bp

@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow_user(username):
    """Logic to follow the user"""
    form = EmptyForm()
    if  form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username)
        )
        if user is None:
            flash(f"Пользователь {username} не найден.")
            return redirect(url_for("index"))
        if user == current_user:
            flash("Вы не можете подписаться на себя!")
            return redirect(url_for("profile.user", username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f"Вы подписались на {username}!")
        return redirect(url_for("profile.user", username=username))
    else:
        return redirect(url_for("index"))
        
@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow_user(username):
    """Logic to unfollow the user"""
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username)
        )
        if user is None:
            flash(f"Пользователь {username} не найден.")
            return redirect(url_for("index"))
        if user == current_user:
            flash("Вы не можете отписаться от себя!")
            return redirect(url_for("profile.user", username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f"Вы отписались от {username}.")
        return redirect(url_for("profile.user", username=username))
    else:
        return redirect(url_for("index"))