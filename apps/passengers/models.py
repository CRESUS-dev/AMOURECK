
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from phonenumber_field.modelfields import PhoneNumberField
from apps.accounts.models import *
from apps.country.models import *
from apps.core.models import *
from apps.customer.models import Customer
from djmoney.models.fields import MoneyField
from djmoney.money import Money

PAYMENT_METHOD =(
    ('CASH','Espèces'),
    ('MM', 'Mobile Money')

)
class Ticket(TimeStampedModel):
    customer = models.ForeignKey(Customer, verbose_name="Nom client", on_delete=models.PROTECT, blank=False, null=False)
    departure_town = models.ForeignKey(Town, verbose_name="Ville de départ", on_delete=models.PROTECT, blank=False, null=False, related_name='departs')
    arrival_town = models.ForeignKey(Town, verbose_name="Ville d'arrivé", on_delete=models.PROTECT, blank=False, null=False,related_name='arrivées')
    departure_date = models.DateField(verbose_name="Date de départ")
    departure_hour = models.TimeField(verbose_name="Heure de départ")
    ticket_price = MoneyField(verbose_name='Montant du billet', max_digits=12, decimal_places=0,default=Money(0, 'XOF'))
    payment_method = models.CharField(verbose_name="Mode de paiement", max_length=50, choices=PAYMENT_METHOD)
    mobile_money_phone_number=PhoneNumberField(verbose_name="Numéro Mobile Money", region="FR", unique=False)
    history = HistoricalRecords()  # ajout de l'historique









