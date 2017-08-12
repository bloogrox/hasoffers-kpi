from django.dispatch import receiver

from stats.signals import offer_does_not_exist


@receiver(offer_does_not_exist)
def on_offer_does_not_exist(sender, offer_id, **kwargs):
    from workers.loaders.tasks.load_offer import load_offer

    load_offer.delay(offer_id)
