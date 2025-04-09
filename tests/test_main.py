import requests
import jwt

ENDPOINT = "http://localhost:8000"
auth_token = ""

# will be getting this from environment variable/AWS secret manager/DB
SECRET_KEY = "your-secret-key"

new_email = "check@example.com"
password = "setup"
user_id = 1

"""Check if the application health is stable"""
def test_pingable():
    health_url = ENDPOINT + "/health"
    response = requests.get(health_url)
    assert response.status_code == 200


"""Test if the login functionality works"""
def test_login():

    login_url = ENDPOINT + "/login"
    payload = { "email": "test@example.com", "password": "testpassword" }

    response = requests.post(url=login_url, json=payload)
    assert response.status_code == 200

    cont_json = response.json()
    global auth_token
    auth_token = cont_json['access_token']

    decoded_data = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
    assert decoded_data['sub'] == payload["email"], f"Expected => {payload['email']}, got => {decoded_data['sub']}"


"""Test if the new user is created successfully"""
def test_create_user():

    new_user_creation = {
        "email" : new_email,
        "password" : password
    }

    create_user_url = ENDPOINT + "/users"

    headers = {
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.post(url=create_user_url, json=new_user_creation, headers=headers)
    assert response.status_code == 200

    cont = response.json()
    global user_id
    user_id = cont['id']
    assert 'id' in cont, "Key 'id' does not exists in response"
    assert 'email' in cont, "Key 'email' does not exists in response"
    assert cont['email'] == new_email, f"Expected => {new_email}', got => {cont['email']}"


"""Test if existing user is fetched successfully"""
def test_get_user():

    get_user_url = ENDPOINT + "/users/" + str(user_id)

    headers = {
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.get(url=get_user_url, headers=headers)
    assert response.status_code == 200

    cont = response.json()
    assert 'id' in cont, "Key 'id' does not exists in response"
    assert 'email' in cont, "Key 'email' does not exists in response"
    assert cont['id'] == user_id, f"Expected => {user_id}', got => {cont['id']}"


"""Test if user is deleted successfully"""
def test_delete_user():
    delete_user_url = ENDPOINT + "/users/"

    headers = {
        'Authorization': f'Bearer {auth_token}'
    }

    payload = { "id": user_id }

    response = requests.delete(url=delete_user_url, headers=headers, json=payload)
    assert response.status_code == 200
