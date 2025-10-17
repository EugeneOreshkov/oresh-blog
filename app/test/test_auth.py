from app.models import User

def test_password():    
    u = User(username='susan', email='susan@example.com')
    u.set_password("securepassword")
    assert u.check_password("securepassword") is True
    assert u.check_password("wrongpassword") is False
    