import shutil

from fastapi import APIRouter, UploadFile

from app.logger import get_logger
from app.tasks.tasks import resize_image

logger = get_logger("images")

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
def upload_image(file: UploadFile):
    image_path = f"app/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)
    logger.info("Загружено изображение: %s", image_path)

    resize_image.delay(image_path)
    logger.debug("Задача resize_image поставлена в очередь: %s", image_path)
