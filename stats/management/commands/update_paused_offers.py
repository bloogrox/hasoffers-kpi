from workers.loaders.tasks.update_paused_offers import update_paused_offers

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        update_paused_offers.delay()
