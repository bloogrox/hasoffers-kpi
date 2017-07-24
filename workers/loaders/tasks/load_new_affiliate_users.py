from hasoffers import Hasoffers

from kpi_notificator import celery_app

from stats.models import AffiliateUser
from django.conf import settings


@celery_app.task
def load_new_affiliate_users():

    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    latest_aff_user = AffiliateUser.objects.all().order_by('-id').first()

    max_id = latest_aff_user.id if latest_aff_user else 0

    params = dict(
        fields=['id', 'email', 'affiliate_id'],
        contain=['Affiliate'],
        filters={'id': {'GREATER_THAN': max_id}},
        limit=1000,
        sort={'id': 'asc'},
    )
    resp = api.AffiliateUser.findAll(**params)

    for ho_user in resp.extract_all():
        db_user = AffiliateUser()
        db_user.id = ho_user.id
        db_user.email = ho_user.email
        db_user.affiliate_id = ho_user.affiliate_id
        db_user.account_manager_id = ho_user.Affiliate['account_manager_id']
        db_user.save()
