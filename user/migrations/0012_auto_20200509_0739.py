# Generated by Django 3.0.6 on 2020-05-09 07:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20200508_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirm_code',
            field=models.UUIDField(default=uuid.UUID('7df185b7-ecb1-4923-92e2-a4a7d731c4a6'), editable=False),
        ),
    ]
