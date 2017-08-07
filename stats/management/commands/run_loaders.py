from workers.loaders.tasks.load_new_offers import load_new_offers
from workers.loaders.tasks.load_new_goals import load_new_goals
from workers.loaders.tasks.load_new_affiliate_users import (
    load_new_affiliate_users)
from workers.loaders.tasks.load_employees import load_employees
from workers.loaders.tasks.update_active_offers import update_active_offers

from django.core.management.base import BaseCommand


def get_system_status():
    from dynamic_preferences.registries import global_preferences_registry
    from stats import dynamic_preferences_registry as preferences

    prefs = global_preferences_registry.manager()
    return prefs[preferences.STATUS]


class Command(BaseCommand):

    def handle(self, *args, **options):
        if get_system_status():
            load_new_offers.delay()
            load_new_goals.delay()
            load_new_affiliate_users.delay()
            load_employees.delay()
            update_active_offers.delay()
