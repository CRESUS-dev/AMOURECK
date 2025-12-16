from django.db import models
from simple_history.models import HistoricalRecords
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from AMOURECK import settings
from apps.core.models import (
    TimeStampedModel,
    NamedModel,
    media_directory_path,
    Currency,
)
from apps.country.models import Country, Agency
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import os
from datetime import datetime
from django.db.models import UniqueConstraint
from apps.accounts.models import CustomUser


class PhoneOperator(TimeStampedModel, NamedModel):
    country = models.ForeignKey(
        Country, verbose_name="Pays", blank=False, null=False, on_delete=models.CASCADE
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Operateur Télephonique"
        constraints = [
            UniqueConstraint(
                fields=("name", "country"), name="unique_country_operator_name"
            )
        ]

    def __str__(self):
        return f"{self.name}-{self.country}"


OPEREATION_TYPE_CHOICE = (
    ("S", "Retrait Client "),
    ("E", "Dépôt Client "),
)


class SimCard(TimeStampedModel):
    operator = models.ForeignKey(
        PhoneOperator,
        verbose_name="Opérateur téléphonique",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="operators",
    )
    number = PhoneNumberField(
        verbose_name="Numéro", region=None, unique=True, blank=False, null=False
    )
    balance = models.DecimalField(
        verbose_name="Solde du compte",
        max_digits=12,
        decimal_places=0,
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name="Devise",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="simcards",
    )

    class Meta:
        verbose_name = "Carte SIM"
        verbose_name_plural = "Cartes SIM"
        constraints = [
            UniqueConstraint(
                fields=("operator", "number"), name="unique_operator_simcard_num"
            )
        ]

    def __str__(self):
        return f"{self.operator}"


class Transfert(TimeStampedModel):
    agency = models.ForeignKey(Agency, verbose_name="Agence", on_delete=models.CASCADE)
    sim_card = models.ForeignKey(
        SimCard,
        verbose_name="SIM",
        on_delete=models.CASCADE,
        related_name="transfert_sim_card",
    )
    operation_type = models.CharField(
        max_length=2, choices=OPEREATION_TYPE_CHOICE, blank=True, null=True
    )
    number = PhoneNumberField(
        verbose_name="Numéro", region=None, unique=False, blank=True, null=False
    )

    amount = models.DecimalField(
        verbose_name="Montant Opération", max_digits=12, decimal_places=0, default=0
    )
    screenshot = models.ImageField(
        verbose_name="Capture d'écran",
        upload_to=media_directory_path,
        blank=True,
        null=True,
    )
    commission_amount = models.DecimalField(
        verbose_name="Montant Commission",
        max_digits=12,
        decimal_places=0,
        default=0,
    )
    balance = models.DecimalField(
        verbose_name="Solde du compte", max_digits=12, decimal_places=0, default=0
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name="Devise",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Transfert"
        verbose_name_plural = "Transferts"

    def __str__(self):
        return f"({self.get_operation_type_display()})  de {self.amount} sur le N° {self.number}  (   SIM -{self.sim_card}) "


class Commission(TimeStampedModel):
    transfer = models.OneToOneField(
        "transferts.Transfert",
        on_delete=models.CASCADE,
        related_name="commission",
        verbose_name="Transfert",
    )
    amount = MoneyField(
        verbose_name="Montant Opération",
        max_digits=12,
        decimal_places=0,
        # default=Money(0, "XOF"),
    )
    agency = models.ForeignKey(Agency, verbose_name="Agence", on_delete=models.CASCADE)
    currency = models.ForeignKey(
        Currency,
        verbose_name="Devise",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Commission {self.amount} pour le transfert #{self.transfer_id}"
