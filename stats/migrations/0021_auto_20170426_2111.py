# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 18:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0020_auto_20170424_2340'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trigger',
            unique_together=set([('offer_id', 'affiliate_id', 'key')]),
        ),
    ]