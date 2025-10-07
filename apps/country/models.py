from django.db import models, connection
from apps.core.models import TimeStampedModel, NamedModel
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from apps.core.mixins.session_user_mixin import SessionUserMixin # custom mixin witch get user, agency_id
from simple_history.models import HistoricalRecords
from django.utils import timezone
import re

# Dictionnaire pays -> devise


# Create your models here.
class Country(TimeStampedModel, NamedModel, SessionUserMixin):
    name = models.CharField(verbose_name="Nom", max_length=255, unique=True)
    iso_code= models.CharField(verbose_name="Code ISO du pays", max_length=2,blank=False, null=False, unique=True)
    currency = models.CharField(verbose_name="Devise",max_length=10)
    is_active = models.BooleanField(default=False)
    history = HistoricalRecords()  # ajout de l'historique
    class Meta:
        verbose_name = "Pays"
        verbose_name_plural = "Pays"


    def __str__(self):
        return f"{self.name} ({self.iso_code})"


class Town(TimeStampedModel, NamedModel, SessionUserMixin):
    country = models.ForeignKey(Country, verbose_name="Pays", on_delete=models.PROTECT, related_name="villes")
    history = HistoricalRecords()  # ajout de l'historique
    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"
        unique_together = ('name', 'country')


    def __str__(self):
        return self.name


class Agency(TimeStampedModel, NamedModel):
    country = models.ForeignKey(Country, verbose_name="Pays", on_delete=models.CASCADE, related_name="agencies")
    code = models.CharField(max_length=10, unique=True)
    history = HistoricalRecords()  # ajout de l'historique
    class Meta:
        verbose_name = "Agence"
        verbose_name_plural = "Agences"
        unique_together = ('name', 'country')

    def created_agency_sequence(self):
        """Crée une séquence PostgreSQL spécifique à cette branche si elle n'existe pas"""
        # Nettoyage du code pour qu'il soit conforme au SQL identifier
        safe_code = re.sub(r'[^A-Za-z0-9_]', '_', self.code.upper())
        sequence_name = f"customer_code_seq_{safe_code}"
        with connection.cursor() as cursor:
            cursor.execute(f"""
                CREATE SEQUENCE IF NOT EXISTS {sequence_name}
                START 1 INCREMENT 1;
            """)

    def save(self, *args, **kwargs):
        creating =self.pk is  None
        super().save(*args, **kwargs)
        if creating:
            self.created_agency_sequence()

    def __str__(self):
        return f"({self.country.name}) {self.name}"
