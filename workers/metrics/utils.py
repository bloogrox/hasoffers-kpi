from stats.models import Offer


def offer_exists_and_monitoring_true(offer_id):
    try:
        offer = Offer.objects.get(pk=offer_id)
        return offer.monitoring
    except Offer.DoesNotExist:
        return False


def get_offer_min_clicks(offer_id):
    from stats.models import Offer
    from metric.models import MinClicks

    try:
        offer = Offer.objects.get(pk=offer_id)
    except Offer.DoesNotExist:
        return 0
    else:
        obj = MinClicks.objects.for_offer(offer.id, offer.categories)
        return obj.value
