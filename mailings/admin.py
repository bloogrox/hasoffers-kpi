from django.contrib import admin

from mailings.models import Recipient


@admin.register(Recipient)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('email', 'active',)
