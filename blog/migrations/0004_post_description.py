# Generated by Django 3.0.6 on 2020-05-09 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200509_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
