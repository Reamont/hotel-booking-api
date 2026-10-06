async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params = {
            "date_from": "2026-09-01",
            "date_to": "2026-10-01"
        }
    )
    print(f"{response.json()=}")

    assert response.status_code == 200