import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangosport.settings")
app = Celery('djangosport', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.task
def ping():
    print("Baddie configured celery")


@app.task
def test(arg):
    from django.core.mail import send_mail
    from django.template.loader import render_to_string

    from news.models import News
    from user.models import User

    import smtplib
    from datetime import datetime, time, timedelta

    print(arg)
    html_message = render_to_string("daily.html", dict(news=News.objects.filter(
                is_breaking=True, date_created__gt=datetime.combine(datetime.today(), time.min) - timedelta(days=1))))
    try:
        send_mail(subject="Daily News", message='', from_email="group801.11@gmail.com",
                  recipient_list=User.objects.values_list("email", flat=True), html_message=html_message)
    except smtplib.SMPTException:
        print(f'Error while sending email')