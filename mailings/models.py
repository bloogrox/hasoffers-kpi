from django.db import models


class Recipient(models.Model):
    email = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
