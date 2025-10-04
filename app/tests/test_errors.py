import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

# @pytest.fixture
# TODO 
