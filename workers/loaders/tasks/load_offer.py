from kpi_notificator import celery_app
from hasoffers import Hasoffers
from django.conf import settings
from workers.persisters.tasks.persist_offer import persist_offer


@celery_app.task
def load_offer(offer_id):
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    ho_offer = api.Offer.findById(id=offer_id).extract_one()

    data = {
        'id': ho_offer.id,
        'name': ho_offer.name
    }
    persist_offer.delay(data)
