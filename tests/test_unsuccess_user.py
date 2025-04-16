import requests

"""Test user not found scenario"""
def test_user_not_found_login(base_url, test_new_credentials):
    login_url = f"{base_url}/login"
    response = requests.post(login_url, json=test_new_credentials)
    assert response.status_code == 401
    assert response.json()['detail'] == "User not found"


"""Test user exists scenario"""
def test_user_exists_create(base_url, test_credentials, auth_headers):
    create_user_url = f"{base_url}/users"
    response = requests.post(url=create_user_url, json=test_credentials, headers=auth_headers)
    assert response.status_code == 409
    assert response.json()['detail'] == "User already exists"


"""Test invalid token scenario"""
def test_invalid_token_create_user(base_url, unauth_headers, test_new_credentials):
    create_user_url = f"{base_url}/users"
    response = requests.post(url=create_user_url, json=test_new_credentials, headers=unauth_headers)
    assert response.status_code == 401
