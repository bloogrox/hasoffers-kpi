from kpi_notificator import celery_app
from stats.models import Trigger, Offer
from workers.notify.tasks.notify_manager import notify_manager
from stats.signals import trigger as trigger_signal


@celery_app.task
def min_cr_trigger(metric):

    offer = Offer.objects.get(pk=metric.offer_id)

    if metric.value < offer.min_cr:
        try:
            filters = dict(
                key=Trigger.KEY_MIN_CR,
                offer_id=metric.offer_id,
                affiliate_id=metric.affiliate_id)
            trigger = Trigger.objects.get(**filters)

            trigger.value = metric.value
            trigger.status = Trigger.PROBLEM
            trigger.save()
        except Trigger.DoesNotExist:
            new_trigger = Trigger()
            new_trigger.key = Trigger.KEY_MIN_CR
            new_trigger.offer_id = metric.offer_id
            new_trigger.affiliate_id = metric.affiliate_id
            new_trigger.value = metric.value
            new_trigger.status = Trigger.PROBLEM
            new_trigger.save()

            notify_manager.delay(new_trigger)

            trigger_signal.send(sender=None, trigger=new_trigger)
