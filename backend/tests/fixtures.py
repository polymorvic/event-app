import pytest
from src.api.routes import app
from src.auth.dependencies import authentication

@pytest.fixture
def authenticated_user(user_factory):
    
    test_user = user_factory(first_name="Tom")
    
    app.dependency_overrides[authentication] = lambda: test_user
    
    yield test_user
    
    app.dependency_overrides[authentication] = {}
