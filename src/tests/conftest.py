import pytest
from fastapi.testclient import TestClient
from main import app


# what is fixture? Apply at test code globally for using testing without import
# Using fixture could increase usability and enhancing module
@pytest.fixture
def client():
    return TestClient(app=app)
