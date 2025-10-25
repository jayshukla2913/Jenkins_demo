import os

# ✅ Set the DATABASE_URL before importing app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app  # Now safe to import

def test_home_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
