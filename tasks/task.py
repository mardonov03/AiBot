from celery import Celery
from fast.internal.core import config

celery = Celery(
    "tasks",
    broker=f"redis://{config.settings.REDIS_HOST}:{config.settings.REDIS_PORT}",
    backend=f"redis://{config.settings.REDIS_HOST}:{config.settings.REDIS_PORT}"
)

celery.conf.timezone = "Asia/Tashkent"
celery.conf.task_routes = {"tasks.*": {"queue": "default"}}
