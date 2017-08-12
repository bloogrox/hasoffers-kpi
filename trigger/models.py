from django.db import models

from stats.models import Metric


class Trigger(models.Model):
    metric = models.ForeignKey(Metric)
    name = models.CharField(max_length=64)
    operator = models.CharField(max_length=10)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TriggerCheck(models.Model):

    OK = 'OK'
    PROBLEM = 'PR'
    STATUSES = (
        (OK, 'OK'),
        (PROBLEM, 'PROBLEM')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    trigger = models.ForeignKey(Trigger)
    status = models.CharField(max_length=2, choices=STATUSES)
    offer_id = models.PositiveIntegerField()
    affiliate_id = models.PositiveIntegerField()

    def __str__(self):
        return (f"#{self.id} trigger={self.trigger}, "
                f"status={self.status}, "
                f"offer_id={self.offer_id}, "
                f"affiliate_id={self.affiliate_id}")
