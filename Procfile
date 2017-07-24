release: python manage.py migrate
web: gunicorn kpi_notificator.wsgi
celery-worker: celery -A kpi_notificator.celery_app:app worker -c 1 -l info
celery-beat: celery -A kpi_notificator.celery_app:app beat -l info
