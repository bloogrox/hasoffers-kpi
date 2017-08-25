import sendgrid
from sendgrid.helpers.mail import Mail, Email, Content
from hasoffers import Hasoffers

from kpi_notificator import celery_app
from django.conf import settings
from stats import models
from mailings.models import Recipient


@celery_app.task
def notify_manager_unapprovement(trigger_check, metric_log):
    print("notify_manager_unapprovement: Starting...")

    offer = models.Offer.objects.get(pk=metric_log.offer_id)

    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

    html = f"""
        Affiliate ID: {metric_log.affiliate_id} was UNAPPROVED from
        offer {offer.name} - lost ${metric_log.value}
    """

    from_email = Email(settings.NETWORK_EMAIL)
    subject = ('Affiliate was PAUSED due to click cost!')
    content = Content("text/html", html)

    for recipient in Recipient.objects.filter(active=True):
        to_email = Email(recipient.email)
        mail = Mail(from_email, subject, to_email, content)
        sg.client.mail.send.post(request_body=mail.get())

    # SEND TO MANAGER
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)
    affiliate = (api.Affiliate
                 .findById(id=metric_log.affiliate_id)
                 .extract_one())
    employee = models.Employee.objects.get(pk=affiliate.account_manager_id)

    email_address = (employee.email
                     if not employee.use_secondary
                     else employee.secondary_email)
    to_email = Email(email_address)
    mail = Mail(from_email, subject, to_email, content)
    res = sg.client.mail.send.post(request_body=mail.get())

    print(f'notify_manager_unapprovement: '
          f'affiliate_id={metric_log.affiliate_id} '
          f'offer_id={metric_log.offer_id} '
          f'trigger_check_id={trigger_check.id}')

    return str(res)
