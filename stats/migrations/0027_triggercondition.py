# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-03 17:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0026_unapprovelog'),
    ]

    operations = [
        migrations.CreateModel(
            name='TriggerCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('operator', models.CharField(max_length=10)),
                ('active', models.BooleanField(default=False)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.Metric')),
            ],
        ),
    ]
