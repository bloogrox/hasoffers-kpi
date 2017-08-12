from django.contrib import admin

import threshold.models


@admin.register(threshold.models.EntityType)
class EntitTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'priority')


@admin.register(threshold.models.Threshold)
class ThresholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'trigger', 'entity_type',
                    'entity_id', 'value')
    list_filter = ('trigger', 'entity_type',)
