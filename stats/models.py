from django.db import models


class Metric(models.Model):
    key = models.CharField(max_length=20)

    def __str__(self):
        return self.key


class MetricLog(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    offer_id = models.IntegerField(db_index=True)
    affiliate_id = models.IntegerField(db_index=True)
    metric = models.ForeignKey(Metric)
    value = models.FloatField()


class Offer(models.Model):

    STATUSES = (
        ('active', 'active'),
        ('pending', 'pending'),
        ('paused', 'paused'),
        ('expired', 'expired'),
        ('deleted', 'deleted')
    )

    name = models.TextField()
    categories_str = models.TextField(default="")

    @property
    def categories(self):
        if self.categories_str:
            return [int(cat_str)
                    for cat_str in self.categories_str.split(',')]
        else:
            return []

    status = models.CharField(max_length=7, choices=STATUSES,
                              default='active', db_index=True)
    last_active_at = models.DateTimeField(auto_now_add=True)

    monitoring = models.BooleanField(default=True)
    gr = models.FloatField(verbose_name='Minimal Goal Conversion Threshold',
                           default=0.0, blank=True, null=True)
    one_goal = models.ForeignKey('Goal', related_name='main_offer',
                                 blank=True, null=True, default=None)

    min_conversions = models.PositiveIntegerField(
        verbose_name='Min Conversions', default=0)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Goal(models.Model):

    STATUSES = (
        ('active', 'active'),
        ('deleted', 'deleted')
    )

    name = models.CharField(max_length=128)
    offer = models.ForeignKey(Offer)
    status = models.CharField(max_length=7, choices=STATUSES,
                              default='active')

    def __str__(self):
        return f'{self.id}: {self.name}'


class AffiliateUser(models.Model):
    affiliate_id = models.IntegerField()
    account_manager_id = models.IntegerField(default=None, blank=True,
                                             null=True)
    email = models.CharField(max_length=64)


class Employee(models.Model):
    email = models.CharField(max_length=64)
    secondary_email = models.CharField(max_length=64, blank=True,
                                       null=True, default=None)
    use_secondary = models.BooleanField(default=False)


class AffiliateCap(models.Model):

    class Meta:
        unique_together = ('offer_id', 'affiliate_id',)

    offer_id = models.PositiveIntegerField()
    affiliate_id = models.PositiveIntegerField()
    conversion_cap = models.PositiveIntegerField()
