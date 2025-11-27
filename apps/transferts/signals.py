from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Transfert, Commission, SimCard
from apps.accounting.models import Accounting


@receiver(post_save, sender=Transfert)
def create_commission_and_accounting(sender, instance, created, **kwargs):
    """
    À chaque création de transfert :
    - créer une Commission (si commission_amount > 0)
    - créer une écriture comptable de type PD liée à cette commission
    """
    # Pas de commission ? on sort
    if not instance.commission_amount or instance.commission_amount.amount == 0:
        return

    # 1) créer ou récupérer la commission
    commission, _created = Commission.objects.get_or_create(
        transfer=instance,
        defaults={
            "amount": instance.commission_amount,
            "agency_id": instance.agency_id,
        },
    )
    # si la commission existe déjà mais que le montant a changé, on met à jour
    if not _created and commission.amount != instance.commission_amount:
        commission.amount = instance.commission_amount
        commission.save()

    # On récupère ou crée l'écriture comptable liée à cette commission
    description = f"Commission du transfert {instance.pk}"
    accounting_entry, created_entry = Accounting.objects.get_or_create(
        commission=commission,  # clé de liaison
        defaults={
            "operation_type": "PD",
            "description": description,
            "amount": commission.amount,
            "agency": instance.agency,
        },
    )
    if not created_entry:
        # si l'écriture existe déjà, on la synchronise avec la commission
        accounting_entry.amount = commission.amount
        accounting_entry.description = description
        accounting_entry.agency = instance.agency
        accounting_entry.save()


# @receiver(pre_save, sender=Transfert)
# def store_old_transfert_data(sender, instance, **kwargs):
#     """get the old data of the instance"""
#     if instance.pk:
#         try:
#             old = Transfert.objects.get(pk=instance.pk)
#             instance._old_amount = old.amount
#             instance._old_commission = old.commission_amount
#             instance._old_operation_type = old.operation_type
#         except Transfert.DoesNotExist:
#             instance._old_amount = None
#             instance._old_commission = None
#             instance._old_operation_type = None
#
#     else:
#         instance._old_amount = None
#         instance._old_commission = None
#         instance._old_operation_type = None

#
# @receiver(post_save, sender=Transfert)
# def calculate_simcard_balance(sender, instance, created, **kwargs):
#     sim = instance.sim_card
#     # Creation case
#     if created:
#         if instance.operation_type == "E":
#             sim.balance += instance.amount + instance.commission_amount
#         elif instance.operation_type == "S":
#             sim.balance -= instance.amount + instance.commission_amount
#
#         sim.save()
#
#         # update case: cancel the old transfer before save the new one
#         old_amount = getattr(instance, "_old_amount", None)
#         old_commission = getattr(instance, "_old_commission", None)
#         old_op = getattr(instance, "_old_operation_type", None)
#
#         # cancel the old transfert effect
#         if old_op == "E":
#             sim.balance -= old_amount + old_commission
#         elif old_op == "S":
#             sim.balance += old_amount + old_commission
#
#         # save the new transfert effect
#         if instance.operation_type == "E":
#             sim.balance += instance.amount + instance.commission_amount
#         elif instance.operation_type == "S":
#             sim.balance -= instance.amount + instance.commission_amount
#         sim.save(update_fields=["balance"])
#
#
# @receiver(post_delete, sender=Transfert)
# def rollback_simcard_balance(sender, instance, **kwargs):
#     sim = instance.sim_card
#
#     if instance.operation_type == "E":
#         sim.balance -= instance.amount + instance.commission_amount
#     elif instance.operation_type == "S":
#         sim.balance += instance.amount + instance.commission_amount
#     sim.save(update_fields=["balance"])
from decimal import Decimal


@receiver(post_save, sender=Transfert)
def calculate_simcard_balance(sender, instance, created, **kwargs):
    if not created:
        return  # aucune action sur update

    sim = instance.sim_card
    amount = instance.amount or Decimal("0")
    commission = instance.commission_amount or Decimal("0")

    if instance.operation_type == "E":
        sim.balance += amount + commission
    elif instance.operation_type == "S":
        sim.balance -= amount + commission

    sim.save(update_fields=["balance"])


@receiver(post_delete, sender=Transfert)
def rollback_simcard_balance(sender, instance, **kwargs):
    sim = instance.sim_card
    amount = instance.amount or Decimal("0")
    commission = instance.commission_amount or Decimal("0")

    if instance.operation_type == "E":
        sim.balance -= amount + commission
    elif instance.operation_type == "S":
        sim.balance += amount + commission

    sim.save(update_fields=["balance"])
