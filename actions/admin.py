from django.contrib import admin
from actions.models import (Action, Operation, Notification,
                            NotificationReceiverType)


class OperationInline(admin.TabularInline):
    model = Operation.actions.through
    extra = 0
    verbose_name = 'Operation'
    verbose_name_plural = 'Operations'


class NotificationInline(admin.StackedInline):
    model = Notification
    extra = 0


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'trigger', 'trigger_status')
    inlines = (
        NotificationInline,
        OperationInline,
    )
    exclude = ('operations',)
    fieldsets = (
        ('Conditions', {'fields': ('trigger', 'trigger_status',)}),
    )


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'title')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject',)


@admin.register(NotificationReceiverType)
class NotificationReceiverTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
