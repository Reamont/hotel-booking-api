from app.repositories.base import BaseRepository
from app.models.users import UsersOrm
from app.schemas.users import User, UserWithHashedPassword
from pydantic import EmailStr
from sqlalchemy import select
from app.repositories.mappers.mappers import UserDataMapper

class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email = email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model, from_attributes=True)