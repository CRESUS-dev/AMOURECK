from django.db import transaction
from decimal import Decimal
from .models import Transfert, SimCard, Commission
from apps.accounting.models import Accounting


class TransfertService:
    """Gestio atomique des transferts et du solde SIM"""

    @staticmethod
    @transaction.atomic
    def create_transfert(
        sim: SimCard, amount, commission_amount, operation_type, agency_id, **kwargs
    ):
        """Crée un transfert et met à jour le solde sur la SIM dans une même transaction"""
        amount = amount or Decimal("0")
        commission = commission_amount or Decimal("0")

        transfert = Transfert.objects.create(
            agency_id=agency_id,
            sim_card=sim,
            amount=amount,
            commission_amount=commission,
            operation_type=operation_type,
            **kwargs
        )
        if operation_type == "E":
            sim.balance += amount + commission
        elif operation_type == "S":
            sim.balance -= amount + commission

        Commission.objects.create(
            agency_id=agency_id,
            transfer=transfert.id,
            amount=commission_amount,
        )

        sim.save(update_fields=["balance"])
        return transfert

    @staticmethod
    @transaction.atomic
    def delete_transfert(transfert: Transfert):
        """Supprime un transfert et restaure le solde associé"""
        sim = transfert.sim_card
        amount = transfert.amount or Decimal("0")
        commission = transfert.commission_amount or Decimal("0")

        if transfert.operation_type == "E":
            sim.balance -= amount + commission
        elif transfert.operation_type == "S":
            sim.balance += amount + commission

        sim.save(update_fields=["balance"])
        transfert.delete()
