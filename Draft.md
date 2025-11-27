from django.db.dispatch import receiver
from django.db.models.signals import post_save
from .models import Transfert

@receiver(sender=Transfert, instance, created, **kwargs)
def creation_commission(post_save, sender):
    if created:
        Accounting.objects.create (
            agency = agency_id,
            operation_type ="PD",
            description =f"commission du tranfert # {self.transfert_id}"
            amount = amount
             
            )   