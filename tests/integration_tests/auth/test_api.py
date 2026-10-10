import pytest

@pytest.mark.parametrize("email, password, status_code", [
    ("k0t@pes.com", "1234", 200),
    ("k0t@pes.com", "1234", 400),
    ("k0t1@pes.com", "1235", 200),
    ("abcde", "1235", 422),
    ("abcde@abc", "1235", 422),
])
async def test_auth_flow(
    email, 
    password, 
    status_code, 
    ac
):
    #register
    response_register = await ac.post(
        "/auth/register",
        json = {
            "email": email,
            "password": password
        }
    )
    assert response_register.status_code == status_code
    if status_code != 200:
        return

    #login
    response_login = await ac.post(
            "/auth/login",
            json = {
                "email": email,
                "password": password
            }
        )
    assert response_login.status_code == 200
    assert ac.cookies["access_token"]

    #me
    response_me = await ac.get("/auth/me")
    assert response_me.status_code == 200
    user = response_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    #logout
    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == 200
    assert "access_token" not in ac.cookies
