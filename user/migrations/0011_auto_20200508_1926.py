# Generated by Django 3.0.6 on 2020-05-08 19:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20200508_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirm_code',
            field=models.UUIDField(default=uuid.UUID('f2b27d5a-9da4-481b-a54e-004160c4ae8e'), editable=False),
        ),
    ]
