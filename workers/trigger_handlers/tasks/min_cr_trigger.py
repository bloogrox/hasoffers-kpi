import operator
from kpi_notificator import celery_app
from stats.models import Trigger
from threshold.models import Threshold
from workers.notify.tasks.notify_manager import notify_manager
from stats.signals import trigger as trigger_signal


@celery_app.task
def min_cr_trigger(metric):

    # trigger_condition = (TriggerCondition.objects
    #                      .get(active=True, metric__key=metric.key))
    # trigger_operator = getattr(operator, trigger_condition.operator)

    # threshold_ = Threshold.objects.for_trigger(trigger_condition, metric)

    # if trigger_operator(metric.value, threshold_.value):
    #     "Problem"
    # else:
    #     "OK"

    # try:
    #     filters = dict(
    #         # todo create new trigger-log model
    #         key=Trigger.KEY_MIN_CR,
    #         offer_id=metric.offer_id,
    #         affiliate_id=metric.affiliate_id)
    #     trigger = Trigger.objects.get(**filters)

    #     trigger.value = metric.value
    #     trigger.status = Trigger.PROBLEM
    #     trigger.save()
    # except Trigger.DoesNotExist:
    #     new_values = {
    #         'key': Trigger.KEY_MIN_CR,
    #         'offer_id': metric.offer_id,
    #         'affiliate_id': metric.affiliate_id,
    #         'value': metric.value,
    #         'status': Trigger.PROBLEM
    #     }
    #     new_trigger = Trigger(**new_values)
    #     new_trigger.save()

    #     notify_manager.delay(new_trigger)

    #     trigger_signal.send(sender=None, trigger=new_trigger)

    pass
