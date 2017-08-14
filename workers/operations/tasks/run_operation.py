from kpi_notificator import celery_app

from workers.notify.tasks.notify_affiliate import notify_affiliate
from workers.notify.tasks.notify_manager import notify_manager
from workers.hasoffers_calls.tasks.unapprove_affiliate_offer import (
    unapprove_affiliate_offer)
from workers.hasoffers_calls.tasks.approve_affiliate_offer import (
    approve_affiliate_offer)
from workers.notify.tasks.notify_affiliate_unapprovement import (
    notify_affiliate_unapprovement)
from workers.notify.tasks.notify_affiliate_approved import (
    notify_affiliate_approved)
from workers.notify.tasks.notify_manager_unapprovement import (
    notify_manager_unapprovement)


@celery_app.task
def run_operation(key, trigger_check, metric_log):
    print(f"run_operation: Running {key} operation with arguments"
          f"trigger - {trigger_check}, metric log - {metric_log}")
    if key == "email_affiliate":
        notify_affiliate.delay(metric_log)
    elif key == "email_affiliate_manager":
        notify_manager.delay(trigger_check, metric_log)
    elif key == "unapprove":
        unapprove_affiliate_offer.delay(trigger_check, metric_log)
        notify_affiliate_unapprovement.delay(trigger_check, metric_log)
        notify_manager_unapprovement.delay(trigger_check, metric_log)
    elif key == "approve":
        approve_affiliate_offer.delay(trigger_check, metric_log)
        notify_affiliate_approved.delay(trigger_check, metric_log)
