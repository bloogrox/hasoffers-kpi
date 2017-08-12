import sendgrid
from sendgrid.helpers.mail import Mail, Email, Content
from hasoffers import Hasoffers

from kpi_notificator import celery_app
from django.conf import settings
from stats import models
from mailings.models import Recipient


@celery_app.task
def notify_manager(trigger_check, metric_log):
    print("notify_manager: Starting...")
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

    html = f"""
    <p>
        offer id: {metric_log.offer_id};
        affiliate id: {metric_log.affiliate_id}
        trigger: {trigger_check.trigger.name};
        value: {metric_log.value};
    </p>
    """

    # todo: put back email actions for manager
    # """
    # <p>
    #     <div>
    #         <a href="{settings.SITE_URL}/notify-affiliate
    # /?trigger_id={trigger.id}" target="_blank">notify affiliate</a></div>
    #     <div><a href="{settings.SITE_URL}/unapprove-affiliate
    # /?trigger_id={trigger.id}" target="_blank">
    # unapprove affiliate now</a></div>
    # </p>
    # """

    from_email = Email(settings.NETWORK_EMAIL)
    subject = (f'Hasoffers notification: '
               f'Affiliate #{metric_log.affiliate_id}; '
               f'Offer #{metric_log.offer_id}; '
               f'{trigger_check.trigger.name}={metric_log.value}')
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

    print('notify_manager: '
          f'affiliate_id={metric_log.affiliate_id} '
          f'offer_id={metric_log.offer_id} '
          f'trigger check={trigger_check.id}')

    return str(res)
