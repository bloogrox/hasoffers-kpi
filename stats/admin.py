from django.contrib import admin

import stats.models
from stats.forms import OfferForm


@admin.register(stats.models.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'monitoring', 'action')
    search_fields = ('id', 'name')
    list_filter = ('monitoring', 'action')
    form = OfferForm


@admin.register(stats.models.Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'offer')
    raw_id_fields = ('offer',)
    search_fields = ('id', 'offer__id',)


@admin.register(stats.models.AffiliateUser)
class AffiliateUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'affiliate_id', 'account_manager_id')
    exclude = ('email',)


@admin.register(stats.models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'secondary_email', 'use_secondary')


@admin.register(stats.models.Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('id', 'key')


@admin.register(stats.models.MetricLog)
class MetricLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime', 'metric', 'value', 'offer_id',
                    'affiliate_id')
    list_filter = ('metric',)
    search_fields = ('metric__key', 'offer_id', 'affiliate_id',)


@admin.register(stats.models.AffiliateCap)
class AffiliateCapAdmin(admin.ModelAdmin):
    list_display = ('offer_id', 'affiliate_id', 'conversion_cap')


@admin.register(stats.models.UnapproveLog)
class UnapproveLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime', 'offer_id', 'affiliate_id')
    search_fields = ('offer_id', 'affiliate_id',)
