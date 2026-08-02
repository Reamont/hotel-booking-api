
from fastapi import APIRouter, HTTPException, Response

from app.schemas.users import UserRequestAdd, UserAdd
from app.services.auth import AuthServices
from app.api.dependencies import UserIdDep
from app.api.dependencies import DBdep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post('/register')
async def register_user(data: UserRequestAdd, db: DBdep):
    hashed_password = AuthServices().hash_password(data.password)
    new_user_data = UserAdd(email = data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()
    return {"status": "OK"}

@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
        db: DBdep,
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthServices().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthServices().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBdep):
    user = await db.users.get_one_or_none(id=user_id)
    return user

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}



        
