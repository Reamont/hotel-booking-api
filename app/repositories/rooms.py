from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import selectinload

from app.exceptions import RoomHasBookingsException, RoomNotFoundException
from app.models.rooms import RoomsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from app.repositories.utils import rooms_ids_for_booking


class RoomRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper
    not_found_exception = RoomNotFoundException

    async def get_filtered_by_time(self, hotel_id, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRelsDataMapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_one_with_rels(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)
        )

        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomWithRelsDataMapper.map_to_domain_entity(model)

    async def delete(self, **filters):
        try:
            await super().delete(**filters)
        except IntegrityError:
            raise RoomHasBookingsException
