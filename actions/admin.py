from django.contrib import admin
from actions.models import Action, Operation


class OperationInline(admin.TabularInline):
    model = Operation.actions.through


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'trigger', 'trigger_status')
    inlines = (OperationInline,)
    exclude = ('operations',)


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'title')
