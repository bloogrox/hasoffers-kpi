# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-23 00:55
from __future__ import unicode_literals

from django.db import migrations


def set_offer_action_off(apps, schema_editor):
    # We can't import the Offer model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Offer = apps.get_model("stats", "Offer")
    for offer in Offer.objects.all():
        offer.action = 'off'
        offer.save()


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0014_auto_20170423_0352'),
    ]

    operations = [
        migrations.RunPython(set_offer_action_off)
    ]
