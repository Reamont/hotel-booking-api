from datetime import date

from app.repositories.base import BaseRepository
from app.models.rooms import RoomsOrm
from app.schemas.rooms import Room

from app.repositories.utils import rooms_ids_for_booking


class RoomRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date, 
            date_to: date
            ):
        rooms_ids_to_get = (rooms_ids_for_booking(date_from, date_to, hotel_id))
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
        