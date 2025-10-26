import time
import jwt

from flask import current_app

from app.models import User
from app import db

class PasswordResetTokenService:
    """Service for generating and verifying password reset tokens."""
    
    def __init__(self, secret_key=None, expires_in=600):
        self.secret_key = secret_key or current_app.config['SECRET_KEY']
        self.expires_in = expires_in

    def generate_token(self, user_id: int) -> str:
        """Generate a JWT token for a user."""

        payload = {
            'reset_password': user_id,
            'exp': time.time() + self.expires_in
        }  

        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            payload = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except: 
            return None
        return db.session.get(User, payload)