from django.db import models
from trigger.models import Trigger, TriggerCheck


class Operation(models.Model):
    key = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Action(models.Model):
    trigger = models.ForeignKey(Trigger)
    trigger_status = models.CharField(max_length=32,
                                      choices=TriggerCheck.STATUSES)
    operations = models.ManyToManyField(Operation, related_name='actions')
