import sendgrid
from sendgrid.helpers.mail import *
from hasoffers import Hasoffers

from kpi_notificator import celery_app
from django.conf import settings
from stats import models
from mailings.models import Recipient


@celery_app.task
def notify_manager_unapprovement(trigger):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

    html = f"""
    <p>
        Offer id: {trigger.offer_id};
        Affiliate id: {trigger.affiliate_id}
        Key: {trigger.key};
        Value: {trigger.value};
    </p>
    """

    from_email = Email(settings.NETWORK_EMAIL)
    subject = f'Affiliate #{trigger.affiliate_id} was unapproved from the offer #{trigger.offer_id}'
    content = Content("text/html", html)

    for recipient in Recipient.objects.filter(active=True):
        to_email = Email(recipient.email)
        mail = Mail(from_email, subject, to_email, content)
        sg.client.mail.send.post(request_body=mail.get())

    # SEND TO MANAGER
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)
    affiliate = api.Affiliate.findById(id=trigger.affiliate_id).extract_one()
    employee = models.Employee.objects.get(pk=affiliate.account_manager_id)

    email_address = employee.email if not employee.use_secondary else employee.secondary_email
    to_email = Email(email_address)
    mail = Mail(from_email, subject, to_email, content)
    res = sg.client.mail.send.post(request_body=mail.get())

    print(f'worker=notify_manager_unapprovement affiliate_id={trigger.affiliate_id} offer_id={trigger.offer_id} trigger_id={trigger.id}')

    return res
