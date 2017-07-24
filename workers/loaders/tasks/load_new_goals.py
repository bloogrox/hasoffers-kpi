from hasoffers import Hasoffers

from kpi_notificator import celery_app

from stats.models import Goal
from django.conf import settings


@celery_app.task
def load_new_goals():

    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    max_goal = Goal.objects.all().order_by('-id').first()

    max_goal_id = max_goal.id if max_goal else 0

    params = dict(
        fields=['id', 'name', 'offer_id'],
        contain=['Offer'],
        filters={'id': {'GREATER_THAN': max_goal_id}},
        limit=1000,
        sort={'id': 'asc'}
    )
    resp = api.Goal.findAll(**params)

    for ho_goal in resp.extract_all():
        db_goal = Goal()
        db_goal.id = ho_goal.id
        db_goal.name = ho_goal.name
        db_goal.offer_id = ho_goal.offer_id
        db_goal.save()
