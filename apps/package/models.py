from django.db import models
from apps.core.models import TimeStampedModel, Currency
from apps.customer.models import CustomUser


from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from phonenumber_field.modelfields import PhoneNumberField
from apps.accounts.models import *
from apps.country.models import *
from apps.core.models import *
from apps.customer.models import Customer
from djmoney.models.fields import MoneyField
from djmoney.money import Money

PAYMENT_METHOD = (
    ("CASH", "Espèces"),
    ("CARD", "Carte bancaire"),
    ("Mobile Money", "Mobile Money"),
)

STATUS = (("PAYE", "Payé"), ("NON_PAYE", "Non payé"))


class Package(TimeStampedModel):
    agency = models.ForeignKey(Agency, verbose_name="Agence", on_delete=models.CASCADE)
    package_code = models.CharField(max_length=50, blank=True, null=True)
    customer = models.ForeignKey(
        Customer,
        verbose_name="Nom client",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    departure_town = models.ForeignKey(
        Town,
        verbose_name="Ville de départ",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="departure_town",
    )
    arrival_town = models.ForeignKey(
        Town,
        verbose_name="Ville d'arrivé",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="arrival_town",
    )
    receiver_name = models.CharField(
        verbose_name="Nom-Prénoms receveur", max_length=120, blank=False, null=False
    )
    receiver_phone = PhoneNumberField(
        verbose_name="Tél receveur",
        region=None,
        unique=False,
        blank=True,
        null=True,
        default="",
    )
    description = models.TextField(
        verbose_name="Description du colis", max_length=500, null=False, blank=False
    )
    package_count = models.PositiveIntegerField(verbose_name="Nombre de colis")
    price = models.DecimalField(
        verbose_name="Prix", max_digits=12, decimal_places=0, blank=False, null=False
    )
    payment_method = models.CharField(
        verbose_name="Mode de paiement",
        max_length=50,
        choices=PAYMENT_METHOD,
        blank=False,
        null=False,
    )
    mobile_money_phone_number = PhoneNumberField(
        verbose_name="Numéro Mobile Money",
        region="FR",
        unique=False,
        blank=True,
        null=True,
        default="",
    )
    status = models.CharField(verbose_name="Statut", max_length=15, choices=STATUS)
    currency = models.ForeignKey(
        Currency,
        verbose_name="Devise",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()  # ajout de l'historique

    class Meta:
        verbose_name = "Colis"
        verbose_name_plural = "Colis"

    def save(self, *args, **kwargs):
        """generate pacakge code if it not exist"""
        if not self.package_code:
            self.package_code = self.generate_package_code()
        super().save(*args, **kwargs)

    def generate_package_code(self):
        """generate package code"""
        import re
        from django.utils import timezone

        safe_code = re.sub(r"[^A-Za-z0-9_]", "_", self.agency.code.upper())
        sequence_name = f"package_code_seq_{safe_code}"
        with connection.cursor() as cursor:
            cursor.execute(f" SELECT nextval('{sequence_name}')")
            next_id = cursor.fetchone()[0]

        year = timezone.now().year
        return f"COLIS-{self.agency.code}-{year}-{next_id:06d}"

    def __str__(self):
        return f"{self.package_code}"
