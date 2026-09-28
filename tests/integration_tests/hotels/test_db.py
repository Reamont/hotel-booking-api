from app.utils.db_manager import DBManager
from app.schemas.hotels import HotelAdd
from app.database import async_session_maker

async def test_add_hotel():
    hotel_data = HotelAdd(title="Отель 1", location="Сочи")
    async with DBManager(session_factory=async_session_maker) as db:
        new_hotel_data = db.hotels.add(hotel_data)
        await db.commit()