from hasoffers import Hasoffers

from kpi_notificator import celery_app

from django.conf import settings
from workers.persisters.tasks.persist_goal import persist_goal


@celery_app.task
def load_goals():

    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    params = dict(
        fields=['id', 'name', 'offer_id'],
        contain=['Offer'],
        limit=10000,
    )
    resp = api.Goal.findAll(**params)

    for ho_goal in resp.extract_all():
        goal = {'id': ho_goal.id, 'name': ho_goal.name, 'offer_id': ho_goal.offer_id}
        persist_goal.delay(goal)
