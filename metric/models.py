from django.db import models
from django.db.models import Q


class EntityType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    priority = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name


class Manager(models.Manager):
    def for_offer(self, offer_id, offer_categories):
        min_clicks = (super(Manager, self).get_queryset()
                     .filter(Q(entity_type__name="Offer",
                               entity_id=offer_id) |
                             Q(entity_type__name="OfferCategory",
                               entity_id__in=offer_categories) |
                             Q(entity_type__name="General"))
                     .order_by('-entity_type__priority')
                     .first())
        if not min_clicks:
            raise MinClicks.DoesNotExist(
                f"no min_click found "
                f"for offer_id={offer_id} or "
                f"or category_id={category_id}")
        return min_clicks


class MinClicks(models.Model):
    entity_type = models.ForeignKey(EntityType)
    entity_id = models.PositiveIntegerField(blank=True, null=True,
                                            default=None)
    value = models.FloatField()

    def __str__(self):
        return (f"entity_type={self.entity_type}, "
                f"entity_id={self.entity_id}, value={self.value}")

    objects = Manager()
