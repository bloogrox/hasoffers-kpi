from django.db import models
from django.db.models import Q
from trigger.models import Trigger


class EntityType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    priority = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name


class ThresholdManager(models.Manager):
    def for_trigger(self, trigger, metric_log, offer_categories):
        threshold = (super(ThresholdManager, self).get_queryset()
                     .filter(trigger=trigger)
                     .filter(Q(entity_type__name="Affiliate",
                               entity_id=metric_log.affiliate_id) |
                             Q(entity_type__name="Offer",
                               entity_id=metric_log.offer_id) |
                             Q(entity_type__name="OfferCategory",
                               entity_id__in=offer_categories) |
                             Q(entity_type__name="General"))
                     .order_by('-entity_type__priority')
                     .first())
        if not threshold:
            raise Threshold.DoesNotExist(
                f"no thresholds found for trigger {trigger}, "
                f"for offer_id={metric_log.offer_id} or "
                f"affiliate_id={metric_log.affiliate_id}")
        return threshold


class Threshold(models.Model):
    trigger = models.ForeignKey(Trigger)
    entity_type = models.ForeignKey(EntityType)
    entity_id = models.PositiveIntegerField(blank=True, null=True,
                                            default=None)
    value = models.FloatField()

    def __str__(self):
        return (f"{self.trigger}, entity_type={self.entity_type}, "
                f"entity_id={self.entity_id}, value={self.value}")

    objects = ThresholdManager()
