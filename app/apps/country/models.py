from django.db import models
from apps.core.models import TimeStampedModel, NamedModel
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Country(TimeStampedModel, NamedModel):

    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"

    def __str__(self):
        return self.name


class Town(TimeStampedModel, NamedModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="villes")

    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"

    def __str__(self):
        return self.name


class Agency(TimeStampedModel, NamedModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="agencies")

    class Meta:
        verbose_name = "Agence"
        verbose_name_plural = "Agences"

    def __str__(self):
        return f"({self.country.name}) {self.name}"
