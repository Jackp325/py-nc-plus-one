
def test_valid_login_returns_200(client, default_seed):
    response = client.post("/api/auth/login", json={"email": "bob@example.com", "password": "password123"})
    assert response.status_code == 200

def test_valid_login_returns_token(client, default_seed):
    response = client.post("/api/auth/login", json={"email": "bob@example.com", "password": "password123"})
    assert response.json()["access_token"]

def test_login_returns_401_for_bad_email(client, default_seed):
    response = client.post("/api/auth/login", json={"email": "rob@example.com", "password": "password123"})
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid email or password"

def test_login_returns_401_for_bad_password(client, default_seed):
    response = client.post("/api/auth/login", json={"email": "bob@example.com", "password": "password"})
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid email or password"

def test_login_with_missing_email_returns_400(client):
    response = client.post("/api/auth/login", json={"password": "password123"})
    assert response.status_code == 400

def test_login_with_missing_password_returns_400(client):
    response = client.post("/api/auth/login", json={"email": "bob@example.com"})
    assert response.status_code == 400