from datetime import date

from fastapi import Query, APIRouter, Body

from app.api.dependencies import PaginationDep
from app.api.dependencies import DBdep

from app.schemas.hotels import Hotel, HotelAdd, HotelPATCH




router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBdep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Расположение отеля"),
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10")
):
    per_page = pagination.per_page or 10
    return await db.hotels.get_filtered_by_time(date_from=date_from,
                                                date_to=date_to, 
                                                location = location,
                                                title = title,
                                                limit = per_page,
                                                offset = (pagination.page - 1) * per_page)
    
@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBdep):
        return await db.hotels.get_one_or_none(id = hotel_id)
 

@router.post("")
async def create_hotel(db: DBdep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "BOgatyi Sochi",
            "location": "Сочи, ул.отелей, 2",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Dubai Fountain",
            "location": "Дубай, ул.отелей, 3",
        }
    }
})
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {'status': 'OK', 'data': hotel}




@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: Hotel, db: DBdep):
    await db.hotels.update(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBdep
):
    db.hotels.update(hotel_data, id = hotel_id, exclude_unset = True)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBdep):
    await db.hotels.delete(id = hotel_id)
    await db.commit()
    return {"status": "OK"}

    