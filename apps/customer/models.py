from django.db import models, connection
from apps.core.models import TimeStampedModel, NamedModel
from phonenumber_field.modelfields import PhoneNumberField
from apps.country.models import Country, Agency, Town
from apps.accounts.models import CustomUser
from simple_history.models import HistoricalRecords
from django.utils import timezone
from django.db import transaction


class Customer(TimeStampedModel):
    SEXE_CHOICE = (
        ("M", "Masculin"),
        ("F", "Féminin"),
    )

    agency = models.ForeignKey(Agency, verbose_name="Agence", on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True, blank=True)
    firstName = models.CharField(
        verbose_name="Prénoms", max_length=150, blank=False, null=False
    )
    lastName = models.CharField(
        verbose_name="Nom", max_length=150, blank=False, null=False
    )
    sex = models.CharField(
        verbose_name="Sexe", max_length=1, choices=SEXE_CHOICE, blank=False, null=False
    )
    phone_number = PhoneNumberField(
        verbose_name="Télephone", region=None, blank=True, unique=True, default=""
    )
    email = models.EmailField(blank=True, default="")
    IDCardNumber = models.CharField(
        verbose_name="N° pièce d'identificaiton",
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        default="",
    )
    address = models.CharField(
        verbose_name="Adresse", max_length=200, blank=True, null=True, default=""
    )
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="Pays")
    history = HistoricalRecords()  # ajout de l'historique

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = " Clients"
        unique_together = (("firstName", "lastName", "phone_number"),)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.code:
            self.code = f"CLT-{self.agency.code}-{self.id:06d}"
            super().save(update_fields=["code"])

    def __str__(self):
        return f"{self.lastName}  {self.firstName}"
