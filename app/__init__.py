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
    Path("app/logs").mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler("app/logs/app.log", maxBytes=10240, backupCount=10, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except Exception as e:
    logger.warning('File logging setup failed: %s', e)

# Email errors in production if SMTP configured
if not app.debug and app.config['MAIL_SERVER']:         
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

from app import routes, models # noqa: F401

from app.avatars import bp as avatars_bp
app.register_blueprint(avatars_bp, url_prefix="/avatars")

from app.profile import bp as profile_bp
app.register_blueprint(profile_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)