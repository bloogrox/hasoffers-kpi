import django.dispatch


trigger = django.dispatch.Signal(providing_args=["trigger"])
offer_does_not_exist = django.dispatch.Signal(providing_args=["offer_id"])
