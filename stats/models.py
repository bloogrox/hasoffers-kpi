from django.db import models


class Metric(models.Model):
    key = models.CharField(max_length=20)

    def __str__(self):
        return self.key


class MetricLog(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    offer_id = models.IntegerField()
    affiliate_id = models.IntegerField()
    metric = models.ForeignKey(Metric)
    value = models.FloatField()


class Offer(models.Model):
    ACTION_OFF = 'off'
    ACTION_ONLY_EMAIL = 'only_email'
    ACTION_PAUSE_IMMEDIATELY = 'pause_immediately'
    ACTION_PAUSE_IN_24H = 'pause_in_24h'
    ACTIONS = (
        (ACTION_OFF, 'Off',),
        (ACTION_ONLY_EMAIL, 'Only Email',),
        (ACTION_PAUSE_IMMEDIATELY, 'Pause Immediately',),
        (ACTION_PAUSE_IN_24H, 'Pause in 24h',)
    )

    name = models.TextField()
    categories_str = models.TextField(default="")

    @property
    def categories(self):
        return [int(cat_str) for cat_str in self.categories_str.split(',')]

    monitoring = models.BooleanField(default=True)
    notify_affiliate = models.BooleanField('Notify Affiliate?',
                                           default=False)
    action = models.CharField(max_length=30, choices=ACTIONS,
                              default=ACTION_OFF)
    gr = models.FloatField(verbose_name='Minimal Goal Conversion Threshold',
                           default=0.0, blank=True, null=True)
    one_goal = models.ForeignKey('Goal', related_name='main_offer',
                                 blank=True, null=True, default=None)

    min_conversions = models.PositiveIntegerField(
        verbose_name='Min Conversions', default=0)
    lookback = models.PositiveIntegerField(
        verbose_name='Lookback Period (days)', default=1)

    min_clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Goal(models.Model):
    name = models.CharField(max_length=128)
    offer = models.ForeignKey(Offer)

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
