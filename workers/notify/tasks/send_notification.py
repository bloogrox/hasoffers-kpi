import datetime
from hasoffers import Hasoffers
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, Personalization
from kpi_notificator import celery_app
from django.conf import settings
from stats.models import Offer, Employee


@celery_app.task
def send_notification(notification, trigger_check, metric_log):
    print('send_notification starting with params: '
          f'notification_id={metric_log.affiliate_id} '
          f'trigger check={trigger_check.id}'
          f'trigger={trigger_check.trigger}')

    to_emails = []
    for receiver in notification.receivers.all():
        if receiver.name == 'Affiliate Manager':
            affiliate = get_affiliate(metric_log.affiliate_id)
            employee = Employee.objects.get(pk=affiliate.account_manager_id)
            email_address = (employee.email
                             if not employee.use_secondary
                             else employee.secondary_email)

            to_emails.append(email_address)

    macros = {
        '{value}': metric_log.value,
        '{offer-id}': metric_log.offer_id,
        '{offer-name}': Offer.objects.get(pk=metric_log.offer_id).name,
        '{affiliate-id}': metric_log.affiliate_id
    }

    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

    mail = Mail()
    mail.from_email = Email(settings.NETWORK_EMAIL)
    subject = notification.subject
    message = notification.message
    for macro, value in macros.items():
        message = message.replace(macro, str(value))
        subject = subject.replace(macro, str(value))
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    message += f"<br><br><small>generated at: {now}</small>"
    mail.subject = subject
    mail.add_content(Content("text/html", message))
    personalization = Personalization()
    for email in to_emails:
        personalization.add_to(Email(email))
    mail.add_personalization(personalization)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(f'send_notification: response.status_code={response.status_code}')
    print(f'send_notification: response.headers={response.headers}')
    print(f'send_notification: response.body={response.body}')

    print('send_notification: '
          f'notification_id={metric_log.affiliate_id} '
          f'trigger check={trigger_check.id}')


def get_affiliate(affiliate_id: int):
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES,
                    retry_count=20)
    affiliate = (api.Affiliate
                 .findById(id=affiliate_id,
                           fields=['id', 'account_manager_id'])
                 .extract_one())
    return affiliate
