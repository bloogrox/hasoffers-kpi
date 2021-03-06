from hasoffers import Hasoffers
from hasoffers import Error
from kpi_notificator import celery_app

from django.conf import settings


@celery_app.task
def approve_affiliate_offer(trigger_check, metric_log):
    print("approve_affiliate_offer: "
          f"offer_id={metric_log.offer_id}"
          f"affiliate_id={metric_log.affiliate_id}")

    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    retry_count=20,
                    proxies=settings.PROXIES)

    params = dict(
        id=metric_log.offer_id,
        affiliate_id=metric_log.affiliate_id,
        status='approved'
    )

    resp = api.Offer.setAffiliateApproval(**params)

    if resp.status != 1:
        raise Error("Error during HasOffers approving call "
                    f"offer_id={metric_log.offer_id} "
                    f"affiliate_id={metric_log.affiliate_id}")
