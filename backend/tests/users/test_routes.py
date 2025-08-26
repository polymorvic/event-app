from fastapi.testclient import TestClient
from src.api.routes import app
from unittest.mock import patch
from src.users.models import User

import pytest

client = TestClient(app)


# @pytest.mark.asyncio
# @patch("src.mail.service.send_verification_mail")
def test_creating_user(db_session):
    # assert db_session.query(Users).count() == 0

    response = client.post(
        "/users/register",
        json={
            "email": "abc@wp.pl",
            "first_name": "Test 123",
            "last_name": "Test Name 123 vbn",
            "password": "qwerty123",
        },
    )

    breakpoint()

    # assert response.status_code == 200
    # assert db_session.query(Users).count() == 1
    # send_verification_mail.assert_called_once()
