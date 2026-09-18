from app.tasks.celery_app import celery_instance
from time import sleep

@celery_instance.task
def test_task():
    sleep(5)
    print("1)")