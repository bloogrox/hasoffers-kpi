# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-12 01:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0004_auto_20170810_0100'),
        ('trigger', '0001_initial')
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='trigger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trigger.Trigger'),
        ),
    ]
