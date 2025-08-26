from fastapi.testclient import TestClient
from src.api.routes import app
from unittest.mock import patch
from src.users.models import User
from src.auth.helpers import generate_verification_token



client = TestClient(app)

@patch("src.users.routes.send_verification_mail")
def test_creating_user(send_verification_mail, db_session):
    
    send_verification_mail.return_value = None
    
    assert db_session.query(User).count() == 0

    response = client.post(
        "/users/register",
        json={
            "email": "przemyslawmarkiewicz97@gmail.com",
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
