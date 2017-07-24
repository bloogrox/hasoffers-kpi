from django.core.management.base import BaseCommand
from dynamic_preferences.registries import global_preferences_registry

# We instantiate a manager for our global preferences
global_preferences = global_preferences_registry.manager()
from stats import dynamic_preferences_registry as preferences


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(global_preferences['non_incent__min_cr'])
        print(global_preferences['non_incent__cap_fill'])
        print(global_preferences['incent__pacc'])
        print(global_preferences['incent__min_clicks'])
        print(preferences.LOOKBACK_PERIOD)
