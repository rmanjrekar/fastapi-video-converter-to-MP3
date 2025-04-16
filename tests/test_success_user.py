import requests
import jwt

"""Check if the application health is stable"""
def test_pingable(base_url):
    health_url = base_url + "/health"
    response = requests.get(health_url)
    assert response.status_code == 200


"""Test if the login functionality works"""
def test_login(auth_token, test_credentials, secret_key):
    decoded_data = jwt.decode(auth_token, secret_key, algorithms=['HS256'])
    assert decoded_data['sub'] == test_credentials["email"]


"""Test if the new user is created successfully"""
def test_create_user(base_url, auth_headers, test_new_credentials):
    create_user_url = f"{base_url}/users"

    response = requests.post(url=create_user_url, json=test_new_credentials, headers=auth_headers)
    assert response.status_code == 200
    cont = response.json()

    global user_id
    user_id = cont['id']

    assert 'id' in cont, "Key 'id' does not exists in response"
    assert 'email' in cont, "Key 'email' does not exists in response"
    assert cont['email'] == test_new_credentials['email'], f"Expected => {test_new_credentials['email']}', got => {cont['email']}"


"""Test if existing user is fetched successfully"""
def test_get_user(base_url, auth_headers):
    get_user_url = f"{base_url}/users/{user_id}"
    response = requests.get(url=get_user_url, headers=auth_headers)
    assert response.status_code == 200

    cont = response.json()
    assert cont['id'] == user_id, f"Expected => {user_id}', got => {cont['id']}"


"""Test if user is deleted successfully"""
def test_delete_user(base_url, auth_headers):
    payload = {"id": user_id}
    delete_user_url = base_url + "/users/"
    response = requests.delete(url=delete_user_url, headers=auth_headers, json=payload)
    assert response.status_code == 200
