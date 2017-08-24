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


class NotificationReceiverType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Notification(models.Model):
    subject = models.CharField(max_length=256)
    message = models.TextField()
    # help_text='Available macroses are: {METRIC.affiliate_id}'
    action = models.ForeignKey(Action, related_name='notifications')
    receivers = models.ManyToManyField(NotificationReceiverType)

    def __str__(self):
        return self.subject
