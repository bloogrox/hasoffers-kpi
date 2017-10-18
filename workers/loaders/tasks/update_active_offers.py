import datetime
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
        offer_categories_ids = list(dict(offer.OfferCategory).keys())

        try:
            db_offer = Offer.objects.get(pk=offer.id)
        except Offer.DoesNotExist:
            pass
        else:
            db_offer.name = offer.name
            db_offer.categories_str = ','.join(offer_categories_ids)
            db_offer.status = 'active'
            db_offer.last_active_at = datetime.datetime.utcnow()
            db_offer.save()
