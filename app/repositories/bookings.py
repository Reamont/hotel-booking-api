from datetime import date

from sqlalchemy import select

from fastapi import HTTPException

from app.repositories.base import BaseRepository
from app.models.bookings import BookingOrm
from app.repositories.mappers.mappers import BookingDataMapper
from app.schemas.bookings import BookingAdd
from app.repositories.utils import rooms_ids_for_booking

class BookingRepository(BaseRepository):
    model = BookingOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id
        )
        rooms_ids_to_get_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_for_book: list[int] = rooms_ids_to_get_res.scalars().all()
        if data.room_id in rooms_ids_for_book:
            new_booking = await self.add(data)
        else:
            raise HTTPException(status_code=403, detail = "Невозможно забронировать данный номер")