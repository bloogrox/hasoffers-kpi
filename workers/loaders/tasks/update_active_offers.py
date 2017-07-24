from hasoffers import Hasoffers
from kpi_notificator import celery_app

from django.conf import settings
from stats.models import Offer


@celery_app.task
def update_active_offers():

    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    params = dict(
        fields=['id', 'name'],
        contain=['OfferCategory'],
        filters={'status': 'active'},
        limit=10000
    )
    resp = api.Offer.findAll(**params)

    for offer in resp.extract_all():
        offer_categories_id = (
            list(
                map(
                    int,
                    list(dict(offer.OfferCategory).keys()))))
        is_incent = bool(set(offer_categories_id) & set(settings.INCENT_CATEGORIES))

        try:
            db_offer = Offer.objects.get(pk=offer.id)
            if db_offer.incent != is_incent:
                db_offer.incent = is_incent
                db_offer.save()
        except Offer.DoesNotExist:
            continue
