from hasoffers import Hasoffers
from kpi_notificator import celery_app
from django.conf import settings

from workers.notify.tasks.notify_affiliate import notify_affiliate
from workers.notify.tasks.notify_manager import notify_manager
from workers.hasoffers_calls.tasks.unapprove_affiliate_offer import (
    unapprove_affiliate_offer)
from workers.hasoffers_calls.tasks.offer_block_affiliate import (
    offer_block_affiliate)
from workers.hasoffers_calls.tasks.approve_affiliate_offer import (
    approve_affiliate_offer)
from workers.notify.tasks.notify_affiliate_unapprovement import (
    notify_affiliate_unapprovement)
from workers.notify.tasks.notify_affiliate_approved import (
    notify_affiliate_approved)
from workers.notify.tasks.notify_manager_unapprovement import (
    notify_manager_unapprovement)
from workers.notify.tasks.notify_manager_approved import (
    notify_manager_approved)


@celery_app.task
def run_operation(key, trigger_check, metric_log):
    print(f"run_operation: Running {key} operation with arguments"
          f"trigger - {trigger_check}, metric log - {metric_log}")
    if key == "email_affiliate":
        notify_affiliate.delay(metric_log)
    elif key == "email_affiliate_manager":
        notify_manager.delay(trigger_check, metric_log)
    elif key == "unapprove":
        if offer_requires_approval(metric_log.offer_id):
            unapprove_affiliate_offer.delay(trigger_check, metric_log)
        else:
            offer_block_affiliate.delay(trigger_check, metric_log)
        notify_affiliate_unapprovement.delay(trigger_check, metric_log)
        notify_manager_unapprovement.delay(trigger_check, metric_log)
    elif key == "approve":
        approve_affiliate_offer.delay(trigger_check, metric_log)
        notify_affiliate_approved.delay(trigger_check, metric_log)
        notify_manager_approved.delay(trigger_check, metric_log)


def offer_requires_approval(offer_id: int) -> bool:
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    retry_count=20,
                    proxies=settings.PROXIES)
    offer = (api.Offer
             .findById(id=offer_id, fields=['id', 'require_approval'])
             .extract_one())
    return True if offer.require_approval == "1" else False
