import sendgrid
from sendgrid.helpers.mail import Mail, Email, Content

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

        from_email = Email("info@performancerevenues.com")
        subject = "Hello World from the SendGrid Python Library!"
        to_email = Email("bloogrox@gmail.com")
        content = Content("text/plain", "Hello, Email!")
        mail = Mail(from_email, subject, to_email, content)

        response = sg.client.mail.send.post(request_body=mail.get())

        print(response.status_code)
        print(response.body)
        print(response.headers)

        to_email2 = Email("a@adsynergy.ru")
        mail2 = Mail(from_email, subject, to_email2, content)
        response = sg.client.mail.send.post(request_body=mail2.get())

        print(response.status_code)
        print(response.body)
        print(response.headers)
