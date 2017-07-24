from kpi_notificator import celery_app
from hasoffers import Hasoffers
from django.conf import settings
from workers.persisters.tasks.persist_offer import persist_offer


@celery_app.task
def load_all_offers():
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    params = dict(
        fields=['id', 'name'],
        limit=10000,
        sort={'id': 'asc'}
    )

    for response in api.Offer.findAll(**params):
        for ho_offer in response.extract_all():
            data = {
                'id': ho_offer.id,
                'name': ho_offer.name
            }
            persist_offer.delay(data)
