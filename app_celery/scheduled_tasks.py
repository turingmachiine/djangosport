from celery.schedules import crontab
from app_celery.celery import app, test


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hours=10, minute=50), test.s("mailing"))

