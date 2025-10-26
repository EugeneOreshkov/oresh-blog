import sqlalchemy as sa
from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app.models import User
from app.service.reset_password.email import send_password_reset_email
from app.service.reset_password.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.service.reset_password.password_reset_service import PasswordResetTokenService

from app import db
from . import bp

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():        
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
            flash('Проверьте вашу почту для дальнейших инструкции по восстановлению пароля')
            return redirect(url_for('auth.login'))
        else:
            flash('К сожалению мы не можем подтвердить вашу личность, проверьте ваши данные ещё раз')
    return render_template('reset_password_request.html', title='Сменить пароль', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = PasswordResetTokenService.verify_reset_password_token(token)
    if not user:
        flash('Недействительная или истекшая ссылка для сброса пароля.')
        return redirect(url_for('auth.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль был сброшен.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)