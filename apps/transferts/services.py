from django.db import transaction
from decimal import Decimal
from .models import Transfert, SimCard, Commission
from apps.accounting.models import Accounting


class TransfertService:
    """Gestio atomique des transferts et du solde SIM"""

    @staticmethod
    @transaction.atomic
    def create_transfert(
        sim_card: SimCard,
        amount,
        commission_amount,
        operation_type,
        agency_id,
        currency_id,
        **kwargs
    ):
        """Crée un transfert et met à jour le solde sur la SIM dans une même transaction"""
        currency = sim_card.currency_id
        amount = amount or Decimal("0")
        commission = commission_amount or Decimal("0")

        # solde avant l'opération
        old_balance = sim_card.balance
        # calcul du nouveau solde

        if operation_type == "E":
            new_balance = old_balance + amount + commission
        elif operation_type == "S":
            new_balance = old_balance - amount + commission
        else:
            raise ValueError("Type d'opération invalide")
            # Mettre à jour la SIM
        sim_card.balance = new_balance
        sim_card.save(update_fields=["balance"])

        transfert = Transfert.objects.create(
            agency_id=agency_id,
            sim_card=sim_card,
            amount=amount,
            commission_amount=commission,
            operation_type=operation_type,
            currency=currency_id,
            balance=new_balance,
            **kwargs
        )

        Commission.objects.create(
            agency_id=agency_id,
            transfer=transfert,
            amount=commission_amount,
            currency_id=currency,
        )

        return transfert
