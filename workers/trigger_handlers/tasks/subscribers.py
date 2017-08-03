import celery_pubsub


# PubSub Subscribtions
celery_pubsub.subscribe('metric.loaded', min_cr_trigger)
