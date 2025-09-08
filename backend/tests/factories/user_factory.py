import pytest
from src.users.models import User


@pytest.fixture
def user_factory(db_session):
    
    def factory(
        email=None,
        first_name=None,
        last_name=None,
        password=None,
        is_admin=False,
        is_activated=True
    ):
        user = User(
            email=email or "test_email@gmail.com",
            first_name=first_name or "John",
            last_name=last_name or "Doe", 
            password=password or "password",
            is_admin=is_admin,
            is_activated=is_activated
        )
        
        db_session.add(user)
        db_session.commit()
        return user
        
    return factory
