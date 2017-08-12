import celery_pubsub

from kpi_notificator import celery_app

from trigger.models import Trigger
from workers.trigger_handlers.tasks.trigger_worker import trigger_worker


@celery_app.task
def trigger_finder(metric_log):
    triggers = (Trigger.objects
                .filter(active=True, metric__key=metric_log.metric.key))

    print(f"trigger_finder: found {triggers} "
          f"for {metric_log.metric.key} metric")

    for trigger in triggers:
        trigger_worker.delay(trigger, metric_log)


# todo: bad place for subscribe
celery_pubsub.subscribe('metric.loaded', trigger_finder)
