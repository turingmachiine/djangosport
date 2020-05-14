import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


def extract_file_extension(filename):
    return filename.split('.')[1]


def upload_img_file(instance, filename: str) -> str:
    user_id = getattr(instance, 'id', None)

    new_filename = '.'.join((str(uuid.uuid4()), extract_file_extension(filename)))
    return f'users/{user_id}/{new_filename}'


class User(AbstractUser):

    class StateEnum(models.TextChoices):
        CONFIRMED = "CONFIRMED"
        NOT_CONFIRMED = "NOT_CONFIRMED"

    profile_pic = models.ImageField(upload_to=upload_img_file, null=True)
    confirm_code = models.UUIDField(default=uuid.uuid4(), editable=False)
    is_confirmed = models.CharField(max_length=255,
                                    choices=StateEnum.choices, default=StateEnum.NOT_CONFIRMED)

    def has_channels(self):
        return len(Channel.objects.filter(owner=self)) > 0

    class Meta:
        db_table = 'site_user'


class Channel(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=255, default="no name")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    description = models.TextField(blank=True)
    followers = models.ManyToManyField(User, blank=True)
