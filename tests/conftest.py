import asyncio
import json
import os

os.environ["MODE"] = "TEST"

from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_db
from app.config import settings
from app.database import Base, async_session_maker_null_pool, engine_null_pool
from app.main import app
from app.models import *
from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAdd
from app.tasks.celery_app import celery_instance
from app.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="module")
async def db_module():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


def load_json(path: str):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    hotels = await asyncio.to_thread(load_json, "tests/mock_hotels.json")
    rooms = await asyncio.to_thread(load_json, "tests/mock_rooms.json")

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
    await ac.post("/auth/register", json={"email": "minimax@mail.ru", "password": "91867527"})


@pytest.fixture(scope="session")
async def authenticated_ac(create_user, ac):
    await ac.post("/auth/login", json={"email": "minimax@mail.ru", "password": "91867527"})
    assert ac.cookies["access_token"]
    yield ac


celery_instance.conf.update(
    task_always_eager=True,
    task_eager_propagates=True,
)
