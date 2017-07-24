# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-24 00:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0017_auto_20170424_0244'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffiliateCap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_id', models.PositiveIntegerField()),
                ('affiliate_id', models.PositiveIntegerField()),
                ('conversion_cap', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='affiliatecap',
            unique_together=set([('offer_id', 'affiliate_id')]),
        ),
    ]
