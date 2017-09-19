from django.contrib import admin

from metric.models import EntityType, MinClicks


@admin.register(EntityType)
class EntitTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'priority')


@admin.register(MinClicks)
class ThresholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'entity_type',
                    'entity_id', 'value')
    list_filter = ('entity_type',)
