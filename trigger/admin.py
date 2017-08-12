from django.contrib import admin

from trigger.models import Trigger


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'metric', 'operator', 'active',)
    list_filter = ('metric', 'active',)
