from django.contrib import admin
from action.models import Action, Operation


# @admin.register(Criteria)
# class CriteriaAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',)

#     class Media:
#         js = ['/static/criteria/js.js']


# class CriteriaInline(admin.TabularInline):
#     model = campaigns.models.CampaignFilter
#     extra = 2


class OperationInline(admin.TabularInline):
    model = Operation.actions.through


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'trigger', 'trigger_status')
    inlines = (OperationInline,)
    exclude = ('operations',)