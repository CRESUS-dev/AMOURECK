
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
    ('CARD','Carte bancaire'),
    ('Mobile Money', 'Mobile Money')
)

STATUS =(
    ('PAYE', 'Payé'),
    ('NON_PAYE', 'Non payé')
)
class Ticket(TimeStampedModel):
    agency = models.ForeignKey(Agency, verbose_name="Agence", on_delete=models.CASCADE)
    ticket_code = models.CharField(max_length=50, blank=True,null=True)
    customer = models.ForeignKey(Customer, verbose_name="Nom client", on_delete=models.CASCADE, blank=False, null=False)
    departure_town = models.ForeignKey(Town, verbose_name="Ville de départ", on_delete=models.CASCADE, blank=False, null=False, related_name='departs')
    arrival_town = models.ForeignKey(Town, verbose_name="Ville d'arrivé", on_delete=models.CASCADE, blank=False, null=False,related_name='arrivées')
    departure_date = models.DateField(verbose_name="Date de départ")
    departure_hour = models.TimeField(verbose_name="Heure de départ")
    ticket_price = MoneyField(verbose_name='Montant du billet', max_digits=12, decimal_places=0,default=Money(0, 'XOF'))
    payment_method = models.CharField(verbose_name="Mode de paiement", max_length=50, choices=PAYMENT_METHOD, blank=False, null=False)
    mobile_money_phone_number=PhoneNumberField(verbose_name="Numéro Mobile Money", region="FR", unique=False, blank=True, null=True,default="")
    status = models.CharField(verbose_name="Statut", max_length= 15, choices=STATUS)
    history = HistoricalRecords()  # ajout de l'historique


    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural ="Tickets"


    def save(self, *args, **kwargs):
        if not self.ticket_code:
            self.ticket_code = self.generate_ticket_code()
        super().save(*args, **kwargs)


    def generate_ticket_code(self):
        """generate ticket code """
        import re
        from django.utils import timezone

        safe_code = re.sub(r'[^A-Za-z0-9_]', '_', self.agency.code.upper())
        sequence_name = f"ticket_code_seq_{safe_code}"
        with connection.cursor() as cursor:
            cursor.execute(f" SELECT nextval('{sequence_name}')")
            next_id = cursor.fetchone()[0]

        year = timezone.now().year
        return f"TCK-{self.agency.code}-{year}-{next_id:06d}"


    def __str__(self):
        return f"{self.ticket_code}"






