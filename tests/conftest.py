import os
import json
os.environ["MODE"] = "TEST"

import pytest

from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAdd
from app.config import settings
from app.database import Base, engine_null_pool
from app.models import *
from httpx import ASGITransport, AsyncClient
from app.main import app

from app.utils.db_manager import DBManager
from app.database import async_session_maker_null_pool


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function")
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_many(hotels)
        await db_.rooms.add_many(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def create_user(ac, setup_database):
    await ac.post("/auth/register", 
        json={
            "email": "minimax@mail.ru",
            "password": "91867527"
            })