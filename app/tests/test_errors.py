import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_404_error(client):
    response = client.get('/nonexistent-route')
    assert response.status_code == 404
    assert b'Page not found.' in response.data