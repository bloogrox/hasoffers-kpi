from functional import seq
from kpi_notificator import celery_app

from workers.trigger_handlers.tasks.capfill_trigger import capfill_trigger
from funcutils import update_in, assoc
from ..utils import offer_exists_and_monitoring_true
from stats.models import Metric, MetricLog, AffiliateCap


def get_conversion_cap(offer_id, affiliate_id):
    try:
        cap = AffiliateCap.objects.get(offer_id=offer_id, affiliate_id=affiliate_id)
        return cap.conversion_cap
    except AffiliateCap.DoesNotExist:
        return 0


def get_prefs():
    return {'lookback': 1}


def get_stats(lookback):
    import pytz
    import datetime
    from hasoffers import Hasoffers
    from django.conf import settings

    from_date = datetime.datetime.now(pytz.timezone(settings.TIME_ZONE)) - datetime.timedelta(days=lookback)
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)
    res = api.Report.getStats(
        fields=['Stat.conversions'],
        groups=['Stat.offer_id', 'Stat.affiliate_id'],
        filters={'Stat.goal_id': {'conditional': 'EQUAL_TO', 'values': 0},
                 'Stat.date': {'conditional': 'GREATER_THAN_OR_EQUAL_TO', 'values': str(from_date.date())},
                 'Stat.hour': {'conditional': 'GREATER_THAN_OR_EQUAL_TO', 'values': from_date.hour}},
        limit=10000)
    return res


@celery_app.task
def get_capfill():

    prefs = get_prefs()
    res = get_stats(prefs['lookback'])

    out = (seq(res.data['data'])
           .map(lambda row: row['Stat'])
           # .filter(lambda row: int(row['clicks']) >= min_clicks)
           .filter(lambda row: offer_exists_and_monitoring_true(row['offer_id']))
           .map(lambda row: update_in(row, ['conversions'], int))
           .map(lambda row: assoc(row, 'conversion_cap', get_conversion_cap(row['offer_id'], row['affiliate_id'])))
           .filter(lambda row: row['conversion_cap'] > 0)
           .map(lambda row: assoc(row, 'value', (row['conversions'] / prefs['lookback']) / row['conversion_cap']))
           .to_list())

    metric = Metric.objects.get(key='cap_fill')

    for row in out:
        metric_log = MetricLog()
        metric_log.offer_id = row['offer_id']
        metric_log.affiliate_id = row['affiliate_id']
        metric_log.metric = metric
        metric_log.value = row['value']
        metric_log.save()

        # run trigger worker
        capfill_trigger.delay(metric_log)
