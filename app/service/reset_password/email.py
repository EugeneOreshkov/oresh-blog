import smtplib
from threading import Thread
import logging

from flask import render_template
from flask_mail import Message

from app import mail, app

logger = logging.getLogger(__name__)

def send_async_email(app, msg):
    smtplib.SMTP.debuglevel = 1
    try:
        with app.app_context():
            mail.send(msg)
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def send_email(subject, sender, recipients, text_body, html_body):
    try:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body    
        Thread(target=send_async_email, args=(app, msg)).start()
    except Exception as e:
        logger.error(f"Failed to create email message: {e}")

def send_password_reset_email(user):
    try:
        token = user.get_reset_token()
        send_email('Brainy - Cброс пароля',
            sender=app.config['MAIL_USERNAME'],
            recipients=[user.email],
            text_body=render_template('reset_password.txt', user=user, token=token),
            html_body=render_template('reset_password_mail.html', user=user, token=token)        
        )
    except Exception as e:
        logger.error(f"Failed to send password reset email to {user.email}: {e}")