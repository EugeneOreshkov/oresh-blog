import os
# Set test environment variables before importing app
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