# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-13 22:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0034_remove_offer_incent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Trigger',
        ),
    ]
