from kpi_notificator import celery_app

from stats.models import Offer


def fetch_global_preferences():
    from dynamic_preferences.registries import global_preferences_registry
    from stats import dynamic_preferences_registry as preferences

    global_preferences = global_preferences_registry.manager()

    prefs = {
        'min_cr': global_preferences[
            preferences.NON_INCENT + '__' + preferences.MIN_CR],
        'max_cr': global_preferences[
            preferences.NON_INCENT + '__' + preferences.MAX_CR],
        'pacc': global_preferences[
            preferences.NON_INCENT + '__' + preferences.PACC],
        'cap_fill': global_preferences[
            preferences.NON_INCENT + '__' + preferences.CAP_FILL],
        'clicks_if_zero_conv': global_preferences[
            preferences.NON_INCENT + '__' + preferences.CLICKS_IF_ZERO_CONV],
        'min_clicks': global_preferences[
            preferences.NON_INCENT + '__' + preferences.MIN_CLICKS],
    }
    return prefs


@celery_app.task
def persist_offer(data):
    """

    Args:
        data: Dict with fields id, name
    """
    prefs = fetch_global_preferences()

    try:
        Offer.objects.get(pk=data['id'])
    except Offer.DoesNotExist:
        db_offer = Offer()
        db_offer.id = data['id']
        db_offer.name = data['name']
        db_offer.categories_str = data['categories_str']

        # initial settings
        for attr, value in prefs.items():
            setattr(db_offer, attr, value)

        db_offer.save()
