from django.core.management.base import BaseCommand

from workers.metrics.tasks.get_capfill import get_capfill
from workers.metrics.tasks.get_cr import get_cr
# from workers.metrics.tasks.get_pacc import get_pacc
from workers.metrics.tasks.get_clicks_if_zero_conv import (
    get_clicks_if_zero_conv)
from workers.metrics.tasks.get_gr import get_gr


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_cr.delay()
        # get_pacc.delay()
        get_clicks_if_zero_conv.delay()
        get_gr.delay()
        get_capfill.delay()
