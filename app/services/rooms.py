from datetime import date

from app.exceptions import check_dates
from app.schemas.facilities import RoomsFacilitiesAdd
from app.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from app.services.base import BaseService


class RoomService(BaseService):
    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        check_dates(date_from, date_to)
        await self.db.hotels.get_one(id=hotel_id)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

    async def create_room(self, hotel_id: int, room_data: RoomAddRequest):
        await self.db.hotels.get_one(id=hotel_id)
        add_room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(add_room_data)

        room_facilities_data = [
            RoomsFacilitiesAdd(room_id=room.id, facility_id=facility_id)
            for facility_id in room_data.facilities_ids or []
        ]
        if room_facilities_data:
            await self.db.rooms_facilities.add_many(room_facilities_data)
        await self.db.commit()
        return room

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        edit_room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.update(edit_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=room_data.facilities_ids or []
        )
        await self.db.commit()

    async def partially_edit_room(self, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
        await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        room_data_dict = room_data.model_dump(exclude_unset=True)
        patch_room_data = RoomPatch(hotel_id=hotel_id, **room_data_dict)
        await self.db.rooms.update(patch_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facilities_ids=room_data_dict["facilities_ids"] or []
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.set_room_facilities(room_id, facilities_ids=[])
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()
