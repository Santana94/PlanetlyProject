from django.db import models
from django.conf import settings

from PlanetlyProject.settings import DEFAULT_MAX_LENGTH


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Usage(AbstractBaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    usage_type = models.ForeignKey("UsageTypes", on_delete=models.CASCADE)
    usage_at = models.DateTimeField()
    amount = models.FloatField()


class UsageTypes(AbstractBaseModel):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    unit = models.CharField(max_length=15)
    factor = models.FloatField()
