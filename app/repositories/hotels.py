from sqlalchemy import select, func

from app.repositories.base import BaseRepository
from app.models.hotels import HotelsOrm
from app.schemas.hotels import Hotel

class HotelRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsOrm)

        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
    
