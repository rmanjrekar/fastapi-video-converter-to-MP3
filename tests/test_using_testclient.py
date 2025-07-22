from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app
from utils.dependencies import get_db
from sqlalchemy.orm import Session
from users.routes import get_current_user

# Mock Session
mock_session = MagicMock(spec=Session)

# Dependency overrides
def override_get_db():
    yield mock_session

def override_get_current_user():
    return MagicMock(email="admin@example.com")

# Set global DB override
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

"""Test: Login Success"""
@patch("users.routes.verify_password", return_value=True)
def test_login_user(mock_verify_password):
    fake_user = MagicMock()
    fake_user.email = "test@example.com"
    fake_user.password = "hashed_pwd"

    mock_session.query().filter().first.return_value = fake_user

    payload = {"email": "test@example.com", "password": "123456"}
    response = client.post("/login", json=payload)

    assert response.status_code == 200


"""Test: Login User Not Found"""
def test_login_user_not_found():
    mock_session.query().filter().first.return_value = None

    payload = {"email": "notfound@example.com", "password": "123456"}
    response = client.post("/login", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "User not found"


"""Test: Login Invalid Password"""
@patch("users.routes.verify_password", return_value=False)
def test_login_user_invalid_password(mock_verify_password):
    fake_user = MagicMock()
    fake_user.email = "test@example.com"
    fake_user.password = "hashed_pwd"

    mock_session.query().filter().first.return_value = fake_user

    payload = {"email": "test@example.com", "password": "wrongpassword"}
    response = client.post("/login", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


"""Test: Create User Success"""
def test_create_user_success():
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_created_user = MagicMock()
    mock_created_user.id = 1
    mock_created_user.email = "newuser@example.com"

    mock_session.query().filter().first.return_value = None
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.side_effect = lambda user: setattr(user, "id", 1)

    new_user_data = {"email": "newuser@example.com", "password": "securepassword"}
    response = client.post("/users", json=new_user_data)

    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"
    assert response.json()["id"] == 1

    app.dependency_overrides.pop(get_current_user, None)


"""Test: User Already Exists"""
def test_create_user_already_exists():
    app.dependency_overrides[get_current_user] = override_get_current_user

    mock_existing_user = MagicMock()
    mock_existing_user.email = "existing@example.com"

    mock_session.query().filter().first.return_value = mock_existing_user

    response = client.post("/users", json={"email": "existing@example.com", "password": "any"})

    assert response.status_code == 409
    assert response.json()["detail"] == "User already exists"

    app.dependency_overrides.pop(get_current_user, None)


"""Test: Empty Payload"""
def test_create_user_empty_payload():
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.post("/users", json={})

    assert response.status_code == 422

    app.dependency_overrides.pop(get_current_user, None)


"""Test: Delete User"""
def test_delete_user_success():
    app.dependency_overrides[get_current_user] = override_get_current_user

    user_to_delete = MagicMock()
    user_to_delete.id = 1
    user_to_delete.email = "userdelete@example.com"
    mock_session.query().filter().first.return_value = user_to_delete

    response = client.request("DELETE", "/users", json={"id": 1})

    assert response.status_code == 200
    assert f"User '{user_to_delete.email}' deleted successfully" in response.json()["detail"]
