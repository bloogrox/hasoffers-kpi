from kpi_notificator import celery_app

from stats.models import Offer


@celery_app.task
def persist_offer(data):
    """

    Args:
        data: Dict with fields id, name
    """
    try:
        Offer.objects.get(pk=data['id'])
    except Offer.DoesNotExist:
        db_offer = Offer()
        db_offer.id = data['id']
        db_offer.name = data['name']
        db_offer.categories_str = data['categories_str']
        db_offer.save()
