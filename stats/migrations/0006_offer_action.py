# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 22:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0005_remove_trigger_metric'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='action',
            field=models.CharField(choices=[('only_email', 'Only Email'), ('pause_immediately', 'Pause Immediately'), ('pause_in_24h', 'Pause in 24h')], default='only_email', max_length=30),
        ),
    ]
