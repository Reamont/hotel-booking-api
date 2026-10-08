from datetime import date

from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.bookings import BookingOrm
from app.repositories.mappers.mappers import BookingDataMapper

class BookingRepository(BaseRepository):
    model = BookingOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]
