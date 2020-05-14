import uuid

from django.db import models
from django.utils import timezone

from user.models import User


def extract_file_extension(filename):
    return filename.split('.')[1]


def upload_img_file(instance, filename: str) -> str:
    news_id = getattr(instance, 'id', None)

    new_filename = '.'.join((str(uuid.uuid4()), extract_file_extension(filename)))
    return f'news/{news_id}/{new_filename}'


class News(models.Model):
    headline = models.CharField(max_length=255)
    news_text = models.TextField()
    source = models.URLField(null=True)
    date_created = models.DateTimeField(default=timezone.now)
    is_breaking = models.BooleanField(default=False)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class NewsComment(models.Model):
    comment_text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

