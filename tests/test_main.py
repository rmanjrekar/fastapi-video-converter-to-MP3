import requests
import jwt

ENDPOINT = "http://localhost:8000"
auth_token = ""

# will be getting this from environment variable/AWS secret manager/DB
SECRET_KEY = "your-secret-key"


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
    new_email = "check7@example.com"
    password = "setup"

    new_user_creation = {
        "email" : new_email,
        "password" : password
    }

    create_url = ENDPOINT + "/users"

    headers = {
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.post(url=create_url, json=new_user_creation, headers=headers)
    assert response.status_code == 200

    cont = response.json()
    assert 'id' in cont, "Key 'id' does not exists in response"
    assert 'email' in cont, "Key 'email' does not exists in response"
    assert cont['email'] == new_email, f"Expected => {new_email}', got => {cont['email']}"
