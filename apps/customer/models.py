from django.db import models
from apps.core.models import TimeStampedModel, NamedModel
from phonenumber_field.modelfields import PhoneNumberField
from apps.country.models import Country
from apps.accounts.models import CustomUser
from simple_history.models import HistoricalRecords


class Customer(TimeStampedModel):
    SEXE_CHOICE = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),

    )

    firstName = models.CharField(verbose_name="Prénoms", max_length=150, blank=False, null=False)
    lastName = models.CharField(verbose_name="Nom", max_length=150, blank=False, null=False)
    sex = models.CharField(verbose_name="Sexe", max_length=1, choices=SEXE_CHOICE, blank=False, null=False)
    phone_number = PhoneNumberField(verbose_name="Télephone", region="FR", unique=True)
    email = models.EmailField(blank=True)
    IDCardNumber = models.CharField(verbose_name="N° pièce d'identificaiton", max_length=100, blank=True, null=True,
                                    unique=True)
    address = models.CharField(verbose_name="Adresse", max_length=200, blank=True, null=True)
    country = models.ForeignKey( Country, on_delete=models.CASCADE,verbose_name="Pays")
    history = HistoricalRecords()  # ajout de l'historique

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = " Clients"
        unique_together = (('firstName', 'lastName', 'phone_number'),)

    def __str__(self):
        return f"{self.lastName}  {self.firstName}"
