from django.core.management.base import BaseCommand

from workers.metrics.tasks.get_capfill import get_capfill
from workers.metrics.tasks.get_cr import get_cr
# from workers.metrics.tasks.get_pacc import get_pacc
from workers.metrics.tasks.get_clicks_if_zero_conv import get_clicks_if_zero_conv
from workers.metrics.tasks.get_gr import get_gr


def get_system_status():
    from dynamic_preferences.registries import global_preferences_registry
    from stats import dynamic_preferences_registry as preferences

    prefs = global_preferences_registry.manager()
    return prefs[preferences.STATUS]


class Command(BaseCommand):

    def handle(self, *args, **options):
        if get_system_status():
            get_cr.delay()
            # get_pacc.delay()
            get_clicks_if_zero_conv.delay()
            get_gr.delay()
            get_capfill.delay()
