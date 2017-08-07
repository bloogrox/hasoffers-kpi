from functional import seq
from kpi_notificator import celery_app

from hasoffers import Hasoffers
from funcutils import update_in
from django.conf import settings
from workers.persisters.tasks.persist_affiliate_cap import (
    persist_affiliate_cap)


@celery_app.task
def load_offer_caps(offer_id):
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    resp = api.Offer.getConversionCaps(id=offer_id)

    if resp.data:
        out = (seq(resp.data.items())
               .map(lambda r: r[1])
               .map(lambda r: r['OfferConversionCap'])
               .map(lambda r: update_in(r, ['offer_id'], int))
               .map(lambda r: update_in(r, ['affiliate_id'], int))
               .map(lambda r: update_in(r, ['conversion_cap'], int))
               .map(lambda r: dict(offer_id=r['offer_id'],
                                   affiliate_id=r['affiliate_id'],
                                   conversion_cap=r['conversion_cap']))
               .to_list()
               )

        for row in out:
            persist_affiliate_cap.delay(row)
