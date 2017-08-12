import pytz
import datetime
from functional import seq
from kpi_notificator import celery_app
import celery_pubsub

from hasoffers import Hasoffers
from funcutils import update_in, assoc
from stats.models import Metric, MetricLog
from django.conf import settings
from ..utils import offer_exists_and_monitoring_true, get_offer_min_clicks


@celery_app.task
def get_clicks_if_zero_conv():
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)

    from_date = (datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
                 - datetime.timedelta(days=1))

    res = api.Report.getStats(
        fields=['Stat.clicks', 'Stat.conversions'],
        groups=['Stat.offer_id', 'Stat.affiliate_id'],
        filters={'Stat.date': {'conditional': 'GREATER_THAN_OR_EQUAL_TO',
                               'values': str(from_date.date())},
                 'Stat.hour': {'conditional': 'GREATER_THAN_OR_EQUAL_TO',
                               'values': from_date.hour}},
        limit=10000)

    out = (seq(res.data['data'])
           .map(lambda row: row['Stat'])
           .filter(lambda row: (
               int(row['clicks']) >= get_offer_min_clicks(row['offer_id'])))
           .filter(lambda row: (
               offer_exists_and_monitoring_true(row['offer_id'])))
           .map(lambda row: update_in(row, ['conversions'], int))
           .map(lambda row: update_in(row, ['clicks'], int))
           .filter(lambda row: row['conversions'] == 0)
           .map(lambda row: assoc(row, 'value', row['clicks']))
           .to_list())

    metric = Metric.objects.get(key='clicks_zero_conv')

    for row in out:
        metric_log = MetricLog()
        metric_log.offer_id = row['offer_id']
        metric_log.affiliate_id = row['affiliate_id']
        metric_log.metric = metric
        metric_log.value = row['value']
        metric_log.save()

        celery_pubsub.publish('metric.loaded', metric_log)
