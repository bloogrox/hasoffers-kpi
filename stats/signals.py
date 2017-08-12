import django.dispatch


offer_does_not_exist = django.dispatch.Signal(providing_args=["offer_id"])
