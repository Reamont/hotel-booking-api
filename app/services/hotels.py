from datetime import date

from app.exceptions import check_dates
from app.schemas.hotels import HotelAdd, HotelPATCH
from app.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        page: int,
        per_page: int,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date,
    ):
        check_dates(date_from, date_to)
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=(page - 1) * per_page,
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.get_one(id=hotel_id)
        await self.db.hotels.update(hotel_data, id=hotel_id)
        await self.db.commit()

    async def partially_edit_hotel(self, hotel_id: int, hotel_data: HotelPATCH):
        await self.db.hotels.get_one(id=hotel_id)
        await self.db.hotels.update(hotel_data, id=hotel_id, exclude_unset=True)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.get_one(id=hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
