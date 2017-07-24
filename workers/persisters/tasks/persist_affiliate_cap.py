from kpi_notificator import celery_app

from stats.models import AffiliateCap


@celery_app.task
def persist_affiliate_cap(data):
    """

    Args:
        data: Dict with fields offer_id, affiliate_id, conversion_cap 
    """
    try:
        db_cap = AffiliateCap.objects.get(offer_id=data['offer_id'], affiliate_id=data['affiliate_id'])

        if db_cap.conversion_cap != data['conversion_cap']:
            db_cap.conversion_cap = data['conversion_cap']
            db_cap.save()
    except AffiliateCap.DoesNotExist:
        new_cap = AffiliateCap()
        new_cap.offer_id = data['offer_id']
        new_cap.affiliate_id = data['affiliate_id']
        new_cap.conversion_cap = data['conversion_cap']
        new_cap.save()
