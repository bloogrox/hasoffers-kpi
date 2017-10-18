import datetime

from django.utils.timezone import utc

from kpi_notificator import celery_app
from stats.models import Offer


@celery_app.task
def update_paused_offers():
    expire_datetime = datetime.datetime.now(utc) - datetime.timedelta(days=1)
    clauses = {
        'status': 'active',
        'last_active_at__lt': expire_datetime
    }
    Offer.objects.filter(**clauses).update(status='paused')
