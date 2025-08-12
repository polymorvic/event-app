from fastapi.testclient import TestClient
from src.api.routes import app
from unittest.mock import patch
import pytest

client = TestClient(app)

@pytest.mark.asyncio
@patch("src.mail.service.send_verification_mail")
async def test_creating_user(send_verification_mail):
    response = client.post("/users/register", json={
        "email": "ssss@wp.pl",
        "first_name": 'Test',
        "last_name": 'Test Name',
        "password": 'qwerty123',
    })
    
    send_verification_mail.assert_called_once()