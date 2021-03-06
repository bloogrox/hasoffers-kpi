import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kpi_notificator.settings')


app = Celery('kpi_notificator',
             # broker="amqp://guest:guest@rabbitmq:5672",
             # backend='amqp://guest:guest@0.0.0.0:5672',
             # include=[]
             )


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks(packages=['workers.hasoffers_calls',
                                 'workers.loaders',
                                 'workers.metrics',
                                 'workers.notify',
                                 'workers.persisters',
                                 'workers.trigger_handlers',
                                 'workers.operations'])


app.conf.task_routes = {
    'workers.hasoffers_calls.tasks.*': {'queue': 'hasoffers'},
    'workers.loaders.tasks.*': {'queue': 'loaders'},
    'workers.metrics.tasks.*': {'queue': 'metrics'},
    'workers.notify.tasks.*': {'queue': 'notifications'},
    'workers.persisters.tasks.*': {'queue': 'persisters'},
    'workers.trigger_handlers.tasks.*': {'queue': 'triggers'},
}


app.conf.beat_schedule = {
    # 'add-every-5-seconds': {
    #     'task': 'tasks.demo.tasks.add.add',
    #     'schedule': 5.0,
    #     'args': (16, 14)
    # },
    'run-metric-get-pacc': {
        'task': 'workers.metrics.tasks.get_pacc.get_pacc',
        'schedule': 120
    },
    'daily-update-offer-status': {
        'task': ('workers.loaders.tasks.update_paused_offers'
                 '.update_paused_offers'),
        'schedule': 60 * 60 * 24
    }
}
