from workers.loaders.tasks.load_new_offers import load_new_offers
from workers.loaders.tasks.load_new_goals import load_new_goals
from workers.loaders.tasks.load_new_affiliate_users import (
    load_new_affiliate_users)
from workers.loaders.tasks.load_employees import load_employees
from workers.loaders.tasks.update_active_offers import update_active_offers

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_new_offers.delay()
        load_new_goals.delay()
        load_new_affiliate_users.delay()
        load_employees.delay()
        update_active_offers.delay()
