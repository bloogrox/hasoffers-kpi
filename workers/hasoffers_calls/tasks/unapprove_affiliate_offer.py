from hasoffers import Hasoffers
from kpi_notificator import celery_app

from django.conf import settings
from stats.models import UnapproveLog


@celery_app.task
def unapprove_affiliate_offer(trigger):
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    retry_count=20,
                    proxies=settings.PROXIES)

    params = dict(
        id=trigger.offer_id,
        affiliate_id=trigger.affiliate_id,
        status='rejected',
        notes=f'reject reason: {trigger.key}'
    )

    resp = api.Offer.setAffiliateApproval(**params)

    if resp.status == 1:
        ul = UnapproveLog()
        ul.offer_id = trigger.offer_id
        ul.affiliate_id = trigger.affiliate_id
        ul.save()
