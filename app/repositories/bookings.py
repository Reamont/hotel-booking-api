from app.repositories.base import BaseRepository
from app.models.bookings import BookingOrm
from app.schemas.bookings import Booking

class BookingRepository(BaseRepository):
    model = BookingOrm
    schema = Booking