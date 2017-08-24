import celery_pubsub
from kpi_notificator import celery_app

from actions.models import Action
from workers.operations.tasks.run_operation import run_operation
from workers.notify.tasks.send_notification import send_notification


@celery_app.task
def trigger_event_worker(trigger_check, metric_log, threshold_):
    print(f"trigger_event_worker: Received Trigger Event {trigger_check} "
          f"{metric_log} {threshold_}")
    actions = (Action.objects
               .filter(trigger=trigger_check.trigger,
                       trigger_status=trigger_check.status))
    for action in actions:
        for operation in action.operations.all():
            run_operation.delay(operation.key, trigger_check, metric_log)
            print(f"trigger_event_worker: Publishing Operation task "
                  f"with args operation.key={operation.key}, "
                  f"{trigger_check}, {metric_log}")
        for notification in action.notifications.all():
            send_notification.delay(notification, trigger_check, metric_log)
            print(f"trigger_event_worker: Notification task "
                  f"with args notification={notification}, "
                  f"{trigger_check}, {metric_log}")


# todo: bad place for subscribe
celery_pubsub.subscribe('trigger-event', trigger_event_worker)
