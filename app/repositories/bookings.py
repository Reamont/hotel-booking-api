from app.repositories.base import BaseRepository
from app.models.bookings import BookingOrm
from app.repositories.mappers.mappers import BookingDataMapper

class BookingRepository(BaseRepository):
    model = BookingOrm
    mapper = BookingDataMapper