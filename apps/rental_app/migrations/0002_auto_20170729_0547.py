# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 05:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='picture',
            field=models.ImageField(default='/img/no-img.jpg', upload_to='img/'),
        ),
    ]
