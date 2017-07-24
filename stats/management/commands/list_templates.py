import sendgrid
from sendgrid.helpers.mail import Email, Content, Substitution, Mail

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

        response = sg.client.templates.get()
        print(response.status_code)
        print(response.body)
        # print(response.headers)
