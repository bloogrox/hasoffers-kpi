import pytz
import datetime
import sendgrid
from kpi_notificator import celery_app

from django.conf import settings
from stats.models import Trigger, AffiliateUser


def fetch_offer(offer_id):
    from hasoffers import Hasoffers

    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)
    resp = api.Offer.findById(id=offer_id, contain=['Thumbnail'])
    offer = resp.extract_one()
    return offer


message_map = {
    Trigger.KEY_MIN_CR: 'low CR',
    Trigger.KEY_MAX_CR: 'high CR',
    Trigger.KEY_PACC: 'low performance',
    Trigger.KEY_MIN_GR: 'low performance',
    Trigger.KEY_CAP_FILL: 'low performance',
    Trigger.KEY_CLICKS_ZERO_CONV: 'low performance'
}


@celery_app.task
def notify_affiliate(trigger, metric_log):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

    offer = fetch_offer(metric_log.offer_id)

    tz = pytz.timezone(settings.TIME_ZONE)

    today = datetime.datetime.now(tz=tz).strftime("%d/%m/%Y")

    # txt = message_map[trigger.key]
    txt = 'low performance'

    aff_users = (AffiliateUser.objects
                 .filter(affiliate_id=metric_log.affiliate_id))

    if aff_users:
        to_ = [{'email': u.email} for u in aff_users]

        data = {
            "personalizations": [
                {
                    "to": to_,
                    "substitutions": {
                        "{firstname}": '',
                        "{message}": txt,
                        "{today}": today,
                        "{offer-id}": str(offer.id),
                        "{offer-name}": offer.name,
                        "{offer-icon-url}": (offer.Thumbnail['thumbnail']
                                             if offer.Thumbnail
                                             else ''),
                        "{offer-preview-url}": offer.preview_url
                    },
                },
            ],
            "from": {
                "email": settings.NETWORK_EMAIL
            },
            "template_id": "2d26917e-cc4e-47a5-a591-71a64b9e65f9"
        }

        res = sg.client.mail.send.post(request_body=data)

        print(f'worker=notify_affiliate affiliate_id={metric_log.affiliate_id} '
              f'offer_id={metric_log.offer_id}')

        return str(res)
