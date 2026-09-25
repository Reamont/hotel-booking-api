from app.services.auth import AuthServices

def test_create_access_token():
    data = {"user_id": 1}
    jwt_token = AuthServices().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

def test_hashed_password():
    data = {"password": "12345643"}
    hashed_password = AuthServices().hash_password(data["password"])

    assert hashed_password
    assert isinstance(hashed_password, str)

