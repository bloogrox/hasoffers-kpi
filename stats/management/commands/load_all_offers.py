from django.core.management.base import BaseCommand
from workers.loaders.tasks.load_all_offers import load_all_offers


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_all_offers.delay()
