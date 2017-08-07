from django.core.management.base import BaseCommand
from stats.models import Offer


def fetch_global_preferences(incent=False):
    from dynamic_preferences.registries import global_preferences_registry
    from stats import dynamic_preferences_registry as preferences

    global_preferences = global_preferences_registry.manager()

    section = preferences.INCENT if incent else preferences.NON_INCENT

    prefs = {
        'min_cr': global_preferences[section + '__' + preferences.MIN_CR],
        'max_cr': global_preferences[section + '__' + preferences.MAX_CR],
        'pacc': global_preferences[section + '__' + preferences.PACC],
        'cap_fill': global_preferences[section + '__' + preferences.CAP_FILL],
        'clicks_if_zero_conv':
            global_preferences[section + '__'
                               + preferences.CLICKS_IF_ZERO_CONV],
        'min_clicks':
            global_preferences[section + '__' + preferences.MIN_CLICKS],
    }
    return prefs


class Command(BaseCommand):

    def handle(self, *args, **options):

        incent_prefs = fetch_global_preferences(incent=True)
        prefs = fetch_global_preferences(incent=False)

        for offer in Offer.objects.all():
            if offer.incent:
                for attr, value in incent_prefs.items():
                    setattr(offer, attr, value)
            else:
                for attr, value in prefs.items():
                    setattr(offer, attr, value)

            offer.save()
