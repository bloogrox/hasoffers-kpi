# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-13 21:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0031_offer_categories_str'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='action',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='action',
            name='action_type',
        ),
        migrations.RemoveField(
            model_name='action',
            name='key',
        ),
        migrations.DeleteModel(
            name='Action',
        ),
    ]