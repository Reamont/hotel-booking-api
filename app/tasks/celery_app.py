from celery import Celery
from celery.signals import setup_logging as celery_setup_logging

from app.config import settings
from app.logger import setup_logging

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "app.tasks.tasks",
    ],
)

celery_instance.conf.beat_schedule = {
    "luboe-nazvanie": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}


@celery_setup_logging.connect
def config_celery_logging(*args, **kwargs):
    # воркер использует наш формат логов вместо стандартного celery
    setup_logging()
