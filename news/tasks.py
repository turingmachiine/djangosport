from datetime import datetime, time, timedelta

from celery.schedules import crontab
from django.conf import settings

from app_celery.celery import app
from news.models import News
from user.models import User
from user.tasks import send_email

