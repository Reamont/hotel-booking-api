from datetime import date


class ApplicationExceptions(Exception):
    status_code: int = 500
    detail: str = "Неожиданная ошибка"

    def __init__(self, detail: str | None = None, *args):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail, *args)


class ObjectNotFoundException(ApplicationExceptions):
    status_code = 404
    detail = "Объект не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class BookingNotFoundException(ObjectNotFoundException):
    detail = "Бронирование не найдено"


class FacilityNotFoundException(ObjectNotFoundException):
    detail = "Удобство не найдено"


class AllRoomsAreBookedException(ApplicationExceptions):
    status_code = 409
    detail = "Не осталось свободных номеров на выбранные даты"


class RoomHasBookingsException(ApplicationExceptions):
    status_code = 409
    detail = "Нельзя удалить номер, на который есть бронирования"


class IncorrectDatesException(ApplicationExceptions):
    status_code = 400
    detail = "Дата выезда должна быть позже даты заезда"


def check_dates(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise IncorrectDatesException
