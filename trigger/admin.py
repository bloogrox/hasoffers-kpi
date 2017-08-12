from django.contrib import admin

from trigger.models import Trigger, TriggerCheck


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'metric', 'operator', 'active',)
    list_filter = ('metric', 'active',)


@admin.register(TriggerCheck)
class TriggerCheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'trigger', 'offer_id',
                    'affiliate_id', 'status',)
    list_filter = ('trigger', 'status', 'offer_id', 'affiliate_id')
