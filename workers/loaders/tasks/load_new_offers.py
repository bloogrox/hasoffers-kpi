from hasoffers import Hasoffers
from stats.models import Offer
from kpi_notificator import celery_app
from django.conf import settings
from workers.persisters.tasks.persist_offer import persist_offer


@celery_app.task
def load_new_offers():

    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    max_offer = Offer.objects.all().order_by('-id').first()

    max_offer_id = max_offer.id if max_offer else 0

    params = dict(
        fields=['id', 'name'],
        contain=['OfferCategory'],
        filters={'id': {'GREATER_THAN': max_offer_id}},
        limit=1000,
        sort={'id': 'asc'},
    )
    resp = api.Offer.findAll(**params)

    for ho_offer in resp.extract_all():
        data = {
            'id': ho_offer.id,
            'name': ho_offer.name
        }
        persist_offer.delay(data)
