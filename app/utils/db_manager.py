from app.logger import get_logger
from app.repositories.bookings import BookingRepository
from app.repositories.facilities import FacilitiesRepository, RoomsFacilitiesRepository
from app.repositories.hotels import HotelRepository
from app.repositories.rooms import RoomRepository
from app.repositories.users import UsersRepository

logger = get_logger("db")


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        logger.debug("Открыта сессия БД")

        self.hotels = HotelRepository(self.session)
        self.rooms = RoomRepository(self.session)
        self.users = UsersRepository(self.session)
        self.bookings = BookingRepository(self.session)
        self.facilities = FacilitiesRepository(self.session)
        self.rooms_facilities = RoomsFacilitiesRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.warning("Откат транзакции из-за %s: %s", exc_type.__name__, exc_val)
            await self.session.rollback()

        await self.session.close()
        logger.debug("Сессия БД закрыта")
        return False

    async def commit(self):
        await self.session.commit()
        logger.debug("Транзакция зафиксирована")
