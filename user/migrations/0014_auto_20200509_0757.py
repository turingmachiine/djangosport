# Generated by Django 3.0.6 on 2020-05-09 07:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20200509_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirm_code',
            field=models.UUIDField(default=uuid.UUID('338c6a21-659f-41f1-9ad4-56af6c8341e0'), editable=False),
        ),
    ]
