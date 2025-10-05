from django.db import models, connection
from apps.core.models import TimeStampedModel, NamedModel
from phonenumber_field.modelfields import PhoneNumberField
from apps.country.models import Country, Agency, Town
from apps.accounts.models import CustomUser
from simple_history.models import HistoricalRecords
from django.utils import timezone



class Customer(TimeStampedModel):
    SEXE_CHOICE = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),

    )

    agency = models.ForeignKey(Agency, verbose_name="Agence", on_delete=models.PROTECT)
    code = models.CharField(max_length=50, unique=True, blank=False, null=True)
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


    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        """Récupère le prochain numéro de la séquence de la branche et génère le code client"""
        sequence_name = f"customer_code_seq_{self.agency.code.upper()}"
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT nextval('{sequence_name}')")
            next_id = cursor.fetchone()[0]
        year = timezone.now().year
        return f"{self.agency.code}-{year}-{next_id:06d}"


    def __str__(self):
        return f"{self.lastName}  {self.firstName}"
