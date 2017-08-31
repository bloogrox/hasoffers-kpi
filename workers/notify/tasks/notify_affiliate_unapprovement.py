import pytz
import datetime
import sendgrid
from hasoffers import Hasoffers
from kpi_notificator import celery_app

from django.conf import settings


def fetch_offer(offer_id):
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES,
                    retry_count=20)

    resp = api.Offer.findById(id=offer_id, contain=['Thumbnail'])
    offer = resp.extract_one()
    return offer


# todo: refactor this
# message_map = {
#     Trigger.KEY_MIN_CR: 'low CR',
#     Trigger.KEY_MAX_CR: 'high CR',
#     Trigger.KEY_PACC: 'low performance',
#     Trigger.KEY_MIN_GR: 'low performance',
#     Trigger.KEY_CAP_FILL: 'low performance',
#     Trigger.KEY_CLICKS_ZERO_CONV: 'low performance'
# }


# todo: refactor according to new input
@celery_app.task
def notify_affiliate_unapprovement(trigger_check, metric_log):
    print("notify_affiliate_unapprovement: Starting...")
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

    offer = fetch_offer(metric_log.offer_id)

    tz = pytz.timezone(settings.TIME_ZONE)

    today = datetime.datetime.now(tz=tz).strftime("%d/%m/%Y")

    now = datetime.datetime.utcnow()

    # txt = message_map[trigger.key]
    txt = 'low performance'

    emails = get_affiliate_emails(metric_log.affiliate_id)

    if emails:
        to_ = [{'email': email} for email in emails]

        data = {
            "personalizations": [
                {
                    "to": to_,
                    "substitutions": {
                        "{firstname}": '',
                        "{today}": today,
                        "{offer-id}": str(metric_log.offer_id),
                        "{offer-name}": offer.name,
                        "{offer-preview-url}": offer.preview_url,
                        "{offer-icon-url}": (offer.Thumbnail['thumbnail']
                                             if offer.Thumbnail else ''),
                        "{message}": txt,
                        "{pause-time}": now.strftime("%d/%m/%Y %H:%M UTC")
                    },
                },
            ],
            "from": {
                "email": settings.NETWORK_EMAIL
            },
            "template_id": "9716e231-6946-4f5c-aded-31397e3ee705"
        }

        res = sg.client.mail.send.post(request_body=data)

        print(f'notify_affiliate_unapprovement: '
              f'affiliate_id={metric_log.affiliate_id} '
              f'offer_id={metric_log.offer_id} '
              f'trigger_check_id={trigger_check.id}')

        return str(res)


def get_affiliate_emails(affiliate_id: int) -> list:
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES,
                    retry_count=20)
    affiliate_users = api.AffiliateUser.findAll(
        fields=['id', 'email'],
        filters={'affiliate_id': affiliate_id, 'status': 'active'}
    ).extract_all()

    return [affiliate_user.email for affiliate_user in affiliate_users]
