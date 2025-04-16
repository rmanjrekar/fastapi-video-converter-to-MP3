import pytest
import requests

ENDPOINT = "http://localhost:8000"
SECRET_KEY = "your-secret-key"


@pytest.fixture(scope="session")
def base_url():
    return ENDPOINT


@pytest.fixture(scope="session")
def secret_key():
    return SECRET_KEY


@pytest.fixture(scope="session")
def test_credentials():
    return {
        "email": "test@example.com",
        "password": "testpassword"
    }


@pytest.fixture(scope="session")
def test_new_credentials():
    return {
        "email": "check@example.com",
        "password": "setup"
    }


@pytest.fixture(scope="session")
def auth_token(base_url, test_credentials):
    login_url = f"{base_url}/login"
    response = requests.post(login_url, json=test_credentials)
    assert response.status_code == 200
    return response.json()['access_token']


@pytest.fixture
def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}"
    }


@pytest.fixture
def unauth_token():
    return "eyJhbGciOiJIUzI1Ni.eyJzdWIiOiJ0ZXN0QGV4YW1wbGU.hQSBkAeBBblMPUZ9j2"


@pytest.fixture
def unauth_headers(unauth_token):
    return {
        "Authorization": f"Bearer {unauth_token}"
    }
