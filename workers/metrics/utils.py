from stats.models import Offer


def offer_exists_and_monitoring_true(offer_id):
    try:
        offer = Offer.objects.get(pk=offer_id)
        return offer.monitoring
    except Offer.DoesNotExist:
        return False


def get_offer_min_clicks(offer_id):
    from stats.models import Offer
    from stats.signals import offer_does_not_exist

    try:
        offer = Offer.objects.get(pk=offer_id)
        return offer.min_clicks
    except Offer.DoesNotExist:
        offer_does_not_exist.send(sender=None, offer_id=offer_id)
