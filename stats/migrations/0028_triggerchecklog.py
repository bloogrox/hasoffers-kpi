# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-09 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0027_triggercondition'),
    ]

    operations = [
        migrations.CreateModel(
            name='TriggerCheckLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('OK', 'OK'), ('PR', 'PROBLEM')], max_length=2)),
                ('trigger_condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.TriggerCondition')),
            ],
        ),
    ]