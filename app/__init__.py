import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flask.logging import default_handler
app.logger.removeHandler(default_handler)

# --- Logging configuration ---
# Ensure logs always go somewhere (console + file), and email on errors in prod
logger = app.logger
logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
logger.propagate = False

formatter = logging.Formatter(
"%(asctime)s - %(levelname)s - %(message)s [in %(pathname)s : %(lineno)d]"    
)

# Console logs 
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

#File logs (rotating)
try:
    logs_dir = Path("app/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "app.log"    
    
    file_handler = RotatingFileHandler(str(log_file), maxBytes=1024000, backupCount=5, encoding="utf-8")

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Logging system initialized successfully")
except Exception as e:
    print(f"File logging setup failed: {e}")
    logger.warning('File logging setup failed: %s', e)

# Email errors in production if SMTP configured
if app.config['MAIL_SERVER']:         
    auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()  

    toaddrs = app.config.get('ADMIN')
    if isinstance(toaddrs, str):
        toaddrs = [toaddrs]

    try:
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']), 
            fromaddr=app.config['MAIL_USERNAME'],
            toaddrs=toaddrs,
            subject='ERROR: Blog Failure',
            credentials=auth,            
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(formatter)
        app.logger.addHandler(mail_handler) 
    except Exception as e:
        logger.warning('SMTPHandler setup failed: %s', e)

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "auth.login"
migrate = Migrate(app, db)
mail = Mail(app)

from app import models, routes # noqa: F401

from app.avatar import bp as avatars_bp
app.register_blueprint(avatars_bp, url_prefix="/avatars")

from app.profile import bp as profile_bp
app.register_blueprint(profile_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.error import bp as errors_bp
app.register_blueprint(errors_bp)

from app.user import bp as users_bp
app.register_blueprint(users_bp)

from app.post import bp as posts_bp
app.register_blueprint(posts_bp)

from app.search import bp as search_bp
app.register_blueprint(search_bp)

from app.service.reset_password import bp as reset_password_bp
app.register_blueprint(reset_password_bp)