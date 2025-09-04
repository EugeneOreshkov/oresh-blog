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
