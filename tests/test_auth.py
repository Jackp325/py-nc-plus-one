
def test_valid_login_returns_200(client, default_seed):
    response = client.post("/api/auth/login", json={"email": "bob@example.com", "password": "password123"})
    assert response.status_code == 200

def test_valid_login_returns_token(client, default_seed):
    response = client.post("/api/auth/login", json={"email": "bob@example.com", "password": "password123"})
    assert response.json()["token"] is not None

def test_login_returns_401_for_bad_email(client, default_seed):
    response = client.post("/api/auth/login", json={"email": "rob@example.com", "password": "password123"})
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid email or password"

def test_login_returns_401_for_bad_password(client, default_seed):
    response = client.post("/api/auth/login", json={"email": "bob@example.com", "password": "password"})
    assert response.status_code == 401
    assert response.json()["error"]["message"] == "Invalid email or password"

def test_login_with_missing_email_returns_400(client, default_seed):
    response = client.post("/api/auth/login", json={"password": "password123"})
    assert response.status_code == 400

def test_login_with_missing_password_returns_400(client, default_seed):
    response = client.post("/api/auth/login", json={"email": "bob@example.com"})
    assert response.status_code == 400

def test_register_returns_201_and_created_user(sample_user):
    response = sample_user
    assert response.status_code == 201
    assert response.json()["user"]["name"] == "Jane Doe"

def test_register_duplicate_email_returns_409(client, sample_user):
    response = client.post("/api/auth/register", json={
        "name": "Jane Doe",
        "email": "j.doe@gmail.com",
        "password": "doedoe123"
    })
    assert response.status_code == 409

def test_register_does_not_return_password(sample_user):
    response = sample_user
    assert "password" not in response.json()["user"]


def test_register_missing_fields_return_400(client, default_seed):
    response = client.post("/api/auth/register", json={
        "name": "Joe Bloggs",
        "email": None,
        "password": "password123"
    })
    assert response.status_code == 400
