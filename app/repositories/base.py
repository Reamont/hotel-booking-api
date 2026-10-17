from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound

from app.exceptions import ObjectNotFoundException
from app.logger import get_logger
from app.repositories.mappers.base import DataMapper

logger = get_logger("repository")


class BaseRepository:
    model = None
    mapper = DataMapper
    not_found_exception: type[ObjectNotFoundException] = ObjectNotFoundException

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            logger.debug("%s: объект не найден по %s", self.model.__name__, filter_by)
            raise self.not_found_exception
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        logger.debug("%s: добавлена запись id=%s", self.model.__name__, model.id)
        return self.mapper.map_to_domain_entity(model)

    async def add_many(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)
        logger.debug("%s: добавлено записей: %s", self.model.__name__, len(data))

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)
        logger.debug("%s: обновление по %s", self.model.__name__, filter_by)

    async def delete(self, **filters):
        delete_stmt = delete(self.model).filter_by(**filters)
        await self.session.execute(delete_stmt)
        logger.debug("%s: удаление по %s", self.model.__name__, filters)
