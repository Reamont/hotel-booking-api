from app.repositories.hotels import HotelRepository
from app.repositories.rooms import RoomRepository
from app.repositories.users import UsersRepository
from app.repositories.bookings import BookingRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelRepository(self.session)
        self.rooms = RoomRepository(self.session)
        self.users = UsersRepository(self.session)
        self.bookings = BookingRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback() 
    
        await self.session.close() 
        return False

    async def commit(self):
        await self.session.commit()

        
