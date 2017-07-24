from workers.loaders.tasks.load_goals import load_goals

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_goals.delay()
