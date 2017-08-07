import pytz
import datetime
from functional import seq
from kpi_notificator import celery_app

from hasoffers import Hasoffers
from funcutils import update_in, assoc
from workers.trigger_handlers.tasks.min_cr_trigger import min_cr_trigger
from workers.trigger_handlers.tasks.max_cr_trigger import max_cr_trigger
from stats.models import Metric, MetricLog
from django.conf import settings
from ..utils import offer_exists_and_monitoring_true, get_offer_min_clicks


def cr(clicks, conversions):
    try:
        return conversions / clicks
    except ZeroDivisionError:
        return 0


def get_stats() -> list:
    """
    @returns
    Example:
    ```
        [
            {
                "Stat": {
                    "conversions": "-194",
                    "clicks": "0",
                    "offer_id": "1650",
                    "affiliate_id": "4358"
                }
            },
            {
                "Stat": {
                    "conversions": "-153",
                    "clicks": "0",
                    "offer_id": "2966",
                    "affiliate_id": "7984"
                }
            }
        ]
    ```
    """
    from_date = (datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
                 - datetime.timedelta(days=1))
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)
    response = api.Report.getStats(
        fields=['Stat.clicks', 'Stat.conversions'],
        groups=['Stat.offer_id', 'Stat.affiliate_id'],
        filters={'Stat.goal_id': {'conditional': 'EQUAL_TO', 'values': 0},
                 'Stat.date': {'conditional': 'GREATER_THAN_OR_EQUAL_TO',
                               'values': str(from_date.date())},
                 'Stat.hour': {'conditional': 'GREATER_THAN_OR_EQUAL_TO',
                               'values': from_date.hour}},
        limit=10000)
    return response.data['data']


@celery_app.task
def get_cr():

    data = get_stats()

    out = (seq(data)
           .map(lambda row: row['Stat'])
           .filter(lambda row: (
               int(row['clicks']) >= get_offer_min_clicks(row['offer_id'])))
           .filter(lambda row: (
               offer_exists_and_monitoring_true(row['offer_id'])))
           .map(lambda row: update_in(row, ['clicks'], int))
           .map(lambda row: update_in(row, ['conversions'], int))
           .map(lambda row: (
               assoc(row, 'value', cr(row['clicks'], row['conversions']))))
           .to_list())

    metric = Metric.objects.get(key='cr')

    for row in out:
        metric_log = MetricLog()
        metric_log.offer_id = row['offer_id']
        metric_log.affiliate_id = row['affiliate_id']
        metric_log.metric = metric
        metric_log.value = row['value']
        metric_log.save()

        min_cr_trigger.delay(metric_log)
        max_cr_trigger.delay(metric_log)
