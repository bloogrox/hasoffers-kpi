from django.http import HttpResponse
from stats import models
from workers.notify.tasks.notify_affiliate import notify_affiliate
from workers.notify.tasks.notify_affiliate_unapprovement import (
    notify_affiliate_unapprovement)
from workers.hasoffers_calls.tasks.unapprove_affiliate_offer import (
    unapprove_affiliate_offer)


def notify_affiliate_about_trigger(request):
    # trigger_id = int(request.GET['trigger_id'])
    # try:
    #     trigger = models.Trigger.objects.get(pk=trigger_id)
    # except models.Trigger.DoesNotExist:
    #     return HttpResponse('Trigger does not exist')

    # notify_affiliate.delay(trigger)

    return HttpResponse('Task is added to the queue')


def unapprove_affiliate_from_offer(request):
    # trigger_id = int(request.GET['trigger_id'])
    # try:
    #     trigger = models.Trigger.objects.get(pk=trigger_id)
    # except models.Trigger.DoesNotExist:
    #     return HttpResponse('Trigger does not exist')

    # unapprove_affiliate_offer.delay(trigger)
    # notify_affiliate_unapprovement.delay(trigger)

    return HttpResponse('Task is added to the queue')
