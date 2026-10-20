from datetime import date
from typing import Annotated

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from app.api.dependencies import DBdep, PaginationDep
from app.schemas.hotels import HotelAdd, HotelPATCH
from app.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=30)
async def get_hotels(
    pagination: PaginationDep,
    db: DBdep,
    *,
    title: Annotated[str | None, Query(description="Название отеля")] = None,
    location: Annotated[str | None, Query(description="Расположение отеля")] = None,
    date_from: Annotated[date, Query(examples=["2024-08-01"])],
    date_to: Annotated[date, Query(examples=["2024-08-10"])],
):
    return await HotelService(db).get_filtered_by_time(
        page=pagination.page,
        per_page=pagination.per_page or 10,
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBdep):
    return await HotelService(db).get_hotel(hotel_id)


@router.post("")
async def create_hotel(
    db: DBdep,
    hotel_data: Annotated[
        HotelAdd,
        Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "BOgatyi Sochi",
                        "location": "Сочи, ул.отелей, 2",
                    },
                },
                "2": {
                    "summary": "Дубай",
                    "value": {
                        "title": "Dubai Fountain",
                        "location": "Дубай, ул.отелей, 3",
                    },
                },
            }
        ),
    ],
):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBdep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBdep):
    await HotelService(db).partially_edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBdep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
