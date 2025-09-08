from fastapi.testclient import TestClient
from src.api.routes import app
from unittest.mock import patch
from src.users.models import User
from src.auth.helpers import generate_verification_token



client = TestClient(app)

@patch("src.users.routes.send_verification_mail")
def test_creating_user(send_verification_mail, db_session):
    assert db_session.query(User).count() == 0

    response = client.post(
        "/users/register",
        json={
            "email": "test_mail@gmail.com",
            "first_name": "Test 123",
            "last_name": "Test Name 123 vbn",
            "password": "qwerty123",
        },
    )
    
    assert db_session.query(User).count() == 1
    user = db_session.query(User).first()
    
    assert user
    
    email_token = generate_verification_token(user.id, user.email)
    
    send_verification_mail.assert_called_once_with(user.email, email_token)

    assert response.status_code == 200
    assert db_session.query(User).count() == 1


def test_user_activate(db_session, user_factory):
    
    user = user_factory(email="testmail@gmail.com", is_activated=False)
    
    assert user.is_activated == False
    
    email_token = generate_verification_token(user.id, user.email)
    

    response = client.get(f"/auth/verify-email/{email_token}")
    
    db_session.refresh(user)

    assert user.is_activated == True
    assert response.status_code == 200
    assert response.json() == {'message': 'Account for user testmail@gmail.com has been activated successfully.'}