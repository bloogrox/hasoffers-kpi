import sendgrid
from typing import List
from hasoffers import Hasoffers
from hasoffers import Error
from hasoffers.mapper import Model
from sendgrid.helpers.mail import Email, Mail, Content, Personalization
from kpi_notificator import celery_app

from django.conf import settings


@celery_app.task
def notify_affiliate_approved(trigger_check, metric_log):
    print("notify_affiliate_approved: Starting...")
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES,
                    retry_count=20)

    affiliate_id = metric_log.affiliate_id
    offer_id = metric_log.offer_id

    offer = get_offer(offer_id, api)

    tr_link = get_tracking_link(offer_id, affiliate_id, api)

    data = {
        "thumbnail": (offer.Thumbnail["thumbnail"]
                      if offer.Thumbnail
                      else None),
        "offer_id": offer.id,
        "offer_name": offer.name,
        "preview_url": offer.preview_url,
        "tracking_link": tr_link,
        "offer_description": offer.description,
    }

    affiliate = get_affiliate_by_id(affiliate_id, api)
    employee = get_employee_by_id(affiliate.account_manager_id, api)

    emails = get_affiliate_emails(affiliate_id, api)
    emails.append(employee.email)

    html = create_content(data)

    config = create_mail_config(
        from_email=settings.NETWORK_EMAIL,
        subject=f"You are approved for the offer #{offer.id}",
        to_emails=emails,
        content=html)

    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

    res = send(config, sg)

    print(f"notify_affiliate_approved: sent email with data {data} "
          f"result {res}")


def get_offer(offer_id: int,
              client: Hasoffers) -> Model:
    return (client.Offer.findById(id=offer_id, contain=["Thumbnail"])
            .extract_one())


def get_tracking_link(offer_id: int,
                      affiliate_id: int,
                      client: Hasoffers) -> str:
    params = dict(offer_id=offer_id, affiliate_id=affiliate_id)
    resp = client.Offer.generateTrackingLink(**params)
    try:
        return resp.data["click_url"]
    except:
        return ''


def get_affiliate_emails(affiliate_id: int, client: Hasoffers) -> List[str]:
    params = dict(fields=["email"],
                  filters={"affiliate_id": affiliate_id, "status": "active"})
    affiliate_users = (client.AffiliateUser
                       .findAll(**params)
                       .extract_all())
    emails = [affiliate_user.email
              for affiliate_user in affiliate_users]
    return emails


def get_affiliate_by_id(affiliate_id: int, client: Hasoffers) -> Model:
    """
    @returns Affiliate object
    """
    try:
        return client.Affiliate.findById(id=affiliate_id).extract_one()
    except Error as e:
        print(f"get_affiliate_by_id: exception {e}")


def get_employee_by_id(employee_id: int, client: Hasoffers) -> Model:
    """
    @returns Employee object
    """
    try:
        return client.Employee.findById(id=employee_id).extract_one()
    except Error as e:
        print(f"get_employee_by_id: exception {e}")


def create_content(data: dict) -> str:
    html = f"""
        <div>
            <a href="{data['preview_url']}" target="_blank">
                <img src="{data['thumbnail']}">
            </a>
        </div>
        <p>#{data['offer_id']}: {data['offer_name']}</p>
        <p>Preview:
            <a href="{data['preview_url']}" target="_blank">
                {data['preview_url']}
            </a>
        </p>
        <p>Tracking link: {data['tracking_link']}</p>
        <p>Description: {data['offer_description']}</p>
    """
    return html


def create_mail_config(from_email: str,
                       subject: str,
                       to_emails: List[str],
                       content: str) -> dict:
    mail = Mail()

    mail.from_email = Email(from_email)
    mail.subject = subject
    personalization = Personalization()
    for email in to_emails:
        personalization.add_to(Email(email))
    mail.add_personalization(personalization)
    mail.add_content(Content("text/html", content))

    return mail.get()


def send(config: dict, client: sendgrid.SendGridAPIClient):
    res = client.client.mail.send.post(request_body=config)
    return res
