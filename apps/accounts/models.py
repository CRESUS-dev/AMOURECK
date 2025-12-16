from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.country.models import *
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
import logging
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from simple_history.models import HistoricalRecords
import os

logger = logging.getLogger(__name__)


def profil_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    base = os.path.splitext(filename)[0]  # nom sans extension
    filename = f"{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return f"profil/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class CustomUser(AbstractUser):
    countries = models.ManyToManyField(
        Country, blank=False, related_name="users_per_country"
    )
    agencies = models.ManyToManyField(
        Agency, blank=False, related_name="users_per_agency"
    )
    profil_picture = models.FileField(
        upload_to=profil_directory_path, blank=True, null=True
    )

    history = HistoricalRecords()  # ajout de l'historique

    def is_admin(self):
        return self.is_superuser  # Vérifier si l'utilisateur est admin

    def __str__(self):
        return self.username

    # vérifier si l'utilisateur a accès à un pays
    def has_access_to_countries(self, country):
        return self.is_superuser or country in self.countries.all()

    # vérifier si l'utilisateur a accès à une agence
    def has_access_to_agencies(self, agency):
        return self.is_superuser or agency in self.agencies.all()

    def validate_relations(self):
        """
        vérifier si l'agence appartient à une pays
        :return:
        """
        if self.countries.exists() and self.agencies.exists():
            for agency in self.agencies.all():
                if agency.country not in self.countries.all():
                    raise ValidationError(
                        f"l'agence {agency} n'appartient pas à une ville assignée"
                    )


# Signal pour valider les relations Many-to-Many
def validate_m2m_relations(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove"]:
        try:
            instance.validate_relations()
        except ValidationError as e:
            logger.error(f"Validation échouée pour l'utilisateur {instance}: {e}")
            instance.countries.clear()
            instance.agencies.clear()

            instance._validation_error = str(e)


# connecter le signal Many-to-Many
m2m_changed.connect(validate_m2m_relations, sender=CustomUser.countries.through)
m2m_changed.connect(validate_m2m_relations, sender=CustomUser.agencies.through)


class LoginHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-login_time"]
        verbose_name = "Historique de connexion"
        verbose_name_plural = "Historiques de connexion"

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"
