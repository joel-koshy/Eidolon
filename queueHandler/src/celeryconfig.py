from celery import Celery

celery_app = Celery(
    "queuehandler",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)
celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
)
