# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_affiliateuser_account_manager_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='monitoring',
            field=models.BooleanField(default=True),
        ),
    ]
