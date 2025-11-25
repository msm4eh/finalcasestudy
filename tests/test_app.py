import os
import tempfile
import pytest
from src.app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    # Check that homepage returns 200 OK
    response = client.get("/")
    assert response.status_code == 200

