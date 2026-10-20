from app.exceptions import check_dates
from app.schemas.bookings import BookingAdd, BookingAddRequest
from app.services.base import BaseService

class BookingService(BaseService):
    async def get_all(self):
        return await self.db.bookings.get_all()

    async def get_me(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(
        self,
        user_id: int,
        booking_data: BookingAddRequest
    ):
        check_dates(booking_data.date_from, booking_data.date_to)
        room = await self.db.rooms.get_one(id=booking_data.room_id)
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room.price,
            **booking_data.model_dump(),
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
        await self.db.commit()
        return booking