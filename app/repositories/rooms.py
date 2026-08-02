from app.repositories.base import BaseRepository
from app.models.rooms import RoomsOrm
from app.schemas.rooms import Room

class RoomRepository(BaseRepository):
    model = RoomsOrm
    schema = Room