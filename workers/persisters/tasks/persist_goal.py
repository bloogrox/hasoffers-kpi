from kpi_notificator import celery_app

from stats.models import Goal


@celery_app.task
def persist_goal(data):
    """

    Args:
        data: Dict with fields id, name, offer_id 
    """
    try:
        Goal.objects.get(pk=data['id'])
    except Goal.DoesNotExist:
        db_goal = Goal()
        db_goal.id = data['id']
        db_goal.name = data['name']
        db_goal.offer_id = data['offer_id']
        db_goal.save()
