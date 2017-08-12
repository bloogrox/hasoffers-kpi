import pytz
import datetime
from functional import seq
from kpi_notificator import celery_app
import celery_pubsub

from hasoffers import Hasoffers
from funcutils import update_in, assoc
from stats.models import Metric, MetricLog, Offer
from django.conf import settings
from ..utils import offer_exists_and_monitoring_true


def gr(conversions, goals):
    try:
        return goals / conversions
    except ZeroDivisionError:
        return 0


def fetch_active_offers():
    """
    Returns: list of offer ids - [1, 2, 3]
    """
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)
    params = dict(
        fields=['id'],
        filters={'status': 'active'},
        limit=10000
    )
    resp = api.Offer.findAll(**params)
    offer_ids = [offer.id for offer in resp.extract_all()]
    return offer_ids


def get_stats(offer_id, goal_id, lookback):
    from_date = (datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
                 - datetime.timedelta(days=lookback))
    api = Hasoffers(network_token=settings.HASOFFERS_NETWORK_TOKEN,
                    network_id=settings.HASOFFERS_NETWORK_ID,
                    proxies=settings.PROXIES)
    response = api.Report.getStats(
        fields=['Stat.conversions'],
        groups=['Stat.offer_id', 'Stat.affiliate_id', 'Stat.goal_id'],
        filters={'Stat.offer_id': {'conditional': 'EQUAL_TO',
                                   'values': offer_id},
                 'Stat.goal_id': {'conditional': 'EQUAL_TO',
                                  'values': [0, goal_id]},
                 'Stat.date': {'conditional': 'GREATER_THAN_OR_EQUAL_TO',
                               'values': str(from_date.date())},
                 'Stat.hour': {'conditional': 'GREATER_THAN_OR_EQUAL_TO',
                               'values': from_date.hour}},
        limit=10000)

    out = (seq(response.data['data'])
           .map(lambda row: row['Stat'])
           .to_list())

    return out


def offer_has_goal(offer_id):
    try:
        offer = Offer.objects.get(pk=offer_id)
    except Offer.DoesNotExist:
        return False

    return bool(offer.one_goal_id)


def get_goals_count(affiliate_id, data):
    res = (seq(data)
           .filter(lambda r: r['affiliate_id'] == affiliate_id)
           .to_list())

    if res:
        return res[0]['conversions']
    else:
        return 0


@celery_app.task
def get_gr():

    print("Gettings GR stats")
    offer_ids = fetch_active_offers()
    offer_ids = list(filter(offer_exists_and_monitoring_true, offer_ids))
    offer_ids = list(filter(offer_has_goal, offer_ids))

    for offer_id in offer_ids:
        offer = Offer.objects.get(pk=offer_id)

        # get stats for the offer
        stats = get_stats(offer_id, offer.one_goal_id, offer.lookback)

        out = (seq(stats)
               .map(lambda row: update_in(row, ['conversions'], int))
               .map(lambda row: update_in(row, ['goal_id'], int))
               .map(lambda row: update_in(row, ['affiliate_id'], int))
               .to_list())

        conversions = seq(out).filter(lambda r: r['goal_id'] == 0).to_list()
        goals = (seq(out)
                 .filter(lambda r: r['goal_id'] == offer.one_goal_id)
                 .to_list())

        # filter min_conversions
        conversions = (
            seq(conversions)
            .filter(lambda r: r['conversions'] >= offer.min_conversions)
            .to_list()
        )

        # populate with goal count
        conversions = (
            seq(conversions)
            .map(lambda r: assoc(r, 'goals',
                                 get_goals_count(r['affiliate_id'], goals)))
            .to_list()
        )

        # populate with gr value
        conversions = (
            seq(conversions)
            .map(lambda r: assoc(r, 'value',
                                 gr(r['conversions'], r['goals'])))
            .to_list()
        )

        # create metric
        metric = Metric.objects.get(key='gtr')

        for row in conversions:
            metric_log = MetricLog()
            metric_log.offer_id = offer_id
            metric_log.affiliate_id = row['affiliate_id']
            metric_log.metric = metric
            metric_log.value = row['value']
            metric_log.save()

            # run trigger worker
            celery_pubsub.publish('metric.loaded', metric_log)
