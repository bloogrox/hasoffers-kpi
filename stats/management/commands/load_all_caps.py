from django.core.management.base import BaseCommand
from workers.loaders.tasks.load_all_caps import load_all_caps


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_all_caps.delay()
