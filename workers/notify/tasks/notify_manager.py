import sendgrid
from sendgrid.helpers.mail import Mail, Email, Content
from hasoffers import Hasoffers

from kpi_notificator import celery_app
from django.conf import settings
from stats import models
from mailings.models import Recipient


@celery_app.task
def notify_manager(trigger):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

    html = f"""
    <p>
        offer id: {trigger.offer_id};
        affiliate id: {trigger.affiliate_id}
        key: {trigger.key};
        value: {trigger.value};
    </p>

    <p>
        <div><a href="{settings.SITE_URL}/notify-affiliate/?trigger_id={trigger.id}" target="_blank">notify affiliate</a></div>
        <div><a href="{settings.SITE_URL}/unapprove-affiliate/?trigger_id={trigger.id}" target="_blank">unapprove affiliate now</a></div>
    </p>
    """

    from_email = Email(settings.NETWORK_EMAIL)
    subject = (f'Hasoffers notification: Affiliate #{trigger.affiliate_id}; '
               f'Offer #{trigger.offer_id}; {trigger.key}={trigger.value}')
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

    email_address = (employee.email
                     if not employee.use_secondary
                     else employee.secondary_email)
    to_email = Email(email_address)
    mail = Mail(from_email, subject, to_email, content)
    res = sg.client.mail.send.post(request_body=mail.get())

    print(f'worker=notify_manager affiliate_id={trigger.affiliate_id} '
          f'offer_id={trigger.offer_id} trigger_id={trigger.id}')

    return str(res)
