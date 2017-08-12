import celery_pubsub
from kpi_notificator import celery_app

from actions.models import Action
from workers.operations.tasks.run_operation import run_operation


@celery_app.task
def trigger_event_worker(trigger_check, metric_log, threshold_):
    actions = (Action.objects
               .filter(trigger=trigger_check.trigger,
                       trigger_status=trigger_check.status))
    # send operation run event
    for action in actions:
        for operation in action.operations.all():
            run_operation.delay(operation.key, trigger_check, metric_log)


# todo: bad place for subscribe
celery_pubsub.subscribe('trigger-event', trigger_event_worker)
