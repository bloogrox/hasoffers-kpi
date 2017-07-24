from kpi_notificator import celery_app
from hasoffers import Hasoffers

from stats.models import Employee
from django.conf import settings


@celery_app.task
def load_employees():
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    resp = api.Employee.findAll(fields=['id', 'email'], limit=1000)

    for ho_employee in resp.extract_all():
        try:
            Employee.objects.get(pk=ho_employee.id)
        except Employee.DoesNotExist:
            db_employee = Employee()
            db_employee.id = ho_employee.id
            db_employee.email = ho_employee.email
            db_employee.save()
