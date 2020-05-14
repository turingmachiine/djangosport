import uuid

from django.db import models
from django.utils import timezone

from user.models import Channel, User


def extract_file_extension(filename):
    return filename.split('.')[1]


def upload_img_file(instance, filename: str) -> str:
    post_id = getattr(instance, 'id', None)

    new_filename = '.'.join((str(uuid.uuid4()), extract_file_extension(filename)))
    return f'posts/{post_id}/{new_filename}'


class Post(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    post_text = models.TextField()
    author = models.ForeignKey(Channel, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    cover = models.ImageField(upload_to=upload_img_file, null=True)


class PostComment(models.Model):
    comment_text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

