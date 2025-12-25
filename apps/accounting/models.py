from django.db import models
from apps.core.models import TimeStampedModel, Currency
from simple_history.models import HistoricalRecords
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from datetime import date
from apps.country.models import Agency

OPEREATION_TYPE_CHOICE = (
    ("PD", "Produits"),
    ("CH", "Charges"),
)


class Accounting(TimeStampedModel):
    agency = models.ForeignKey(Agency, verbose_name="Agence", on_delete=models.PROTECT)
    operation_type = models.CharField(
        max_length=5,
        verbose_name="Type opération",
        choices=OPEREATION_TYPE_CHOICE,
        blank=False,
        null=False,
    )
    date_operation = models.DateField(verbose_name="Date opération", default=date.today)
    description = models.CharField(
        max_length=500, verbose_name="Description", blank=False, null=False
    )
    amount = models.DecimalField(
        verbose_name="Montant", max_digits=12, decimal_places=0, default=Money(0, "XOF")
    )
    commission = models.OneToOneField(
        "transferts.Commission",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="accounting_entry",
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name="Devise",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )
