# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-18 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0044_goal_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('pending', 'pending'), ('paused', 'paused'), ('expired', 'expired'), ('deleted', 'deleted')], default='active', max_length=7),
        ),
    ]
