from app import app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash

@app.shell_context_processor
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                Post=Post,
                so=so,
                sa=sa,
                set_hash=generate_password_hash,
                check=check_password_hash)