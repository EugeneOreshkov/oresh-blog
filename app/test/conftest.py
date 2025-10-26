import os

os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only'

import pytest
from app import app, db 

@pytest.fixture
def client():
    """Create a test client for the application."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
   
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def user_pair(client):
    """Create a test user pair."""
    from app.models import User
    user1 = User(username='user1', email='user1@example.com', phone='1234567890')
    user2 = User(username='user2', email='user2@example.com', phone='1234567891')
    user1.set_password('password123')
    user2.set_password('password123')

    db.session.add_all([user1, user2])
    db.session.commit()

    return user1, user2

