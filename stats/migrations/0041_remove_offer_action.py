# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-17 17:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0040_remove_offer_notify_affiliate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='action',
        ),
    ]