from typing import Annotated
from fastapi import HTTPException

from fastapi import Depends, Query, Request
from pydantic import BaseModel

from app.services.auth import AuthServices
from app.utils.db_manager import DBManager
from app.database import async_session_maker


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Отсутствие токена аутентификации")
    return token

def get_current_user_id(token: str = Depends(get_token)):
    data = AuthServices().decode_jwt(token=token)
    return data["user_id"]

UserIdDep = Annotated[int, Depends(get_current_user_id)]



async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBdep = Annotated[DBManager, Depends(get_db)]