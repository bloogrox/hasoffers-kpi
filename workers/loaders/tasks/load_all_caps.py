from kpi_notificator import celery_app
from hasoffers import Hasoffers
from django.conf import settings
from workers.loaders.tasks.load_offer_caps import load_offer_caps


@celery_app.task
def load_all_caps():
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    params = dict(
        fields=['id'],
        filters={'status': 'active'},
        limit=1000
    )

    resp = api.Offer.findAll(**params)

    for offer in resp.extract_all():
        load_offer_caps.delay(offer.id)
