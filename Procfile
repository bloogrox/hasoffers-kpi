# release: python manage.py migrate
web: gunicorn kpi_notificator.wsgi
celery-worker: celery -A kpi_notificator.celery_app:app worker -c 1 -l info
celery-hasoffers-worker: celery -A kpi_notificator.celery_app:app worker -Q hasoffers -c 1 -l info
celery-loaders-worker: celery -A kpi_notificator.celery_app:app worker -Q loaders -c 1 -l info
celery-metrics-worker: celery -A kpi_notificator.celery_app:app worker -Q metrics -c 1 -l info
celery-triggers-worker: celery -A kpi_notificator.celery_app:app worker -Q triggers -c 3 -l info
celery-notifications-worker: celery -A kpi_notificator.celery_app:app worker -Q notifications -c 1 -l info
celery-persisters-worker: celery -A kpi_notificator.celery_app:app worker -Q persisters -c 1 -l info
celery-beat: celery -A kpi_notificator.celery_app:app beat -l info
