import operator
import celery_pubsub

from kpi_notificator import celery_app

from trigger.models import Trigger, TriggerCheck
from threshold.models import Threshold


@celery_app.task
def trigger_worker(metric_log):
    trigger = (Trigger.objects
               .get(active=True, metric__key=metric_log.metric.key))
    print(f"trigger_worker: processing trigger {trigger}")

    trigger_operator = getattr(operator, trigger.operator)

    threshold_ = Threshold.objects.for_trigger(trigger, metric_log)
    print(f"trigger_worker: using threshold {threshold_}")

    if trigger_operator(metric_log.value, threshold_.value):
        status = TriggerCheck.PROBLEM
    else:
        status = TriggerCheck.OK

    # Prev trigger check
    filters = {
        'trigger': trigger,
        'offer_id': metric_log.offer_id,
        'affiliate_id': metric_log.affiliate_id
    }
    prev_check = (TriggerCheck.objects
                  .filter(**filters)
                  .order_by('-created_at')
                  .first())

    # Log trigger check
    values = {
        'trigger': trigger,
        'offer_id': metric_log.offer_id,
        'affiliate_id': metric_log.affiliate_id,
        'status': status
    }

    trigger_check = TriggerCheck(**values)
    trigger_check.save()

    print(f"trigger_worker: trigger check done {trigger_check}")

    # Trigger Event
    if prev_check:
        if status != prev_check.status:
            celery_pubsub.publish('trigger-event',
                                  trigger_check, metric_log, threshold_)
            print(f"trigger_worker: trigger-event published "
                  f"with params {trigger_check} {metric_log} {threshold_}")
    else:
        if status == TriggerCheck.PROBLEM:
            celery_pubsub.publish('trigger-event',
                                  trigger_check, metric_log, threshold_)
            print(f"trigger_worker: trigger-event published "
                  f"with params {trigger_check} {metric_log} {threshold_}")

    # trigger
    # if (status == Trigger.PROBLEM
    #     and TriggerCheckLog.objects.filter(**values).count() == 1):
    #     # first time problem
    #     trigger_signal.send(sender=None,
    #                         trigger_check_log=trigger_check_log,
    #                         metric=metric,
    #                         threshold=threshold_)


# todo: bad place for subscribe
celery_pubsub.subscribe('metric.loaded', trigger_worker)
