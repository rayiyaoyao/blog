# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-16 06:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20160914_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 16, 6, 22, 48, 158306, tzinfo=utc)),
            preserve_default=False,
        ),
    ]