# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-18 00:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0045_offer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='last_active_at',
            field=models.DateTimeField(default=datetime.datetime(2010, 1, 1, 0, 0, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
