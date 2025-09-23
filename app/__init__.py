
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)
app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "auth.login"
migrate = Migrate(app, db)

from app import routes, models # noqa: F401

from app.avatars import bp as avatars_bp
app.register_blueprint(avatars_bp, url_prefix="/avatars")

from app.profile import bp as profile_bp
app.register_blueprint(profile_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

# --- Logging configuration ---
# Ensure logs always go somewhere (console + file), and email on errors in prod
logger = app.logger
logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

# Avoid duplicating handlers if reloading
if not logger.handlers:
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )

    # Console logs
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File logs (rotating)
    try:
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / 'app.log', maxBytes=10240, backupCount=10, encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        # If file logging fails, at least keep console logging
        logger.warning('File logging setup failed: %s', e)

# Email errors in production if SMTP configured
if not app.debug and app.config.get('MAIL_SERVER'):
    auth = None
    if app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD'):
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config.get('MAIL_USE_TLS'):
        secure = ()

    # Support comma-separated ADMIN list
    toaddrs = app.config.get('ADMIN')
    if isinstance(toaddrs, str):
        toaddrs_list = [addr.strip() for addr in toaddrs.split(',') if addr.strip()]
    else:
        toaddrs_list = [toaddrs] if toaddrs else []

    if toaddrs_list:
        try:
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_USERNAME'],
                toaddrs=toaddrs_list,
                subject='ERROR: Blog Failure',
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            logger.addHandler(mail_handler)
        except Exception as e:
            logger.warning('SMTPHandler setup failed: %s', e)
