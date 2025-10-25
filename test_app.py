import os
import pytest
from app import app

@pytest.fixture(scope="module", autouse=True)
def set_test_env():
    # Mock the DB URL so app doesn't fail to start
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

def test_home_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
