from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import intcomma


@admin.register(PhoneOperator)
class PhoneOperatorAdmin(admin.ModelAdmin):
    model = PhoneOperator
    list_display = ["country", "name"]


@admin.register(SimCard)
class SimCardAdmin(admin.ModelAdmin):
    model = SimCard
    list_display = ["operator", "number", "balance", "currency", "assigned_to"]


@admin.register(Transfert)
class TransfertAdmin(admin.ModelAdmin):
    model = Transfert
    list_display = (
        "agency",
        "sim_card",
        "number",
        "operation_type",
        "amount_display",
        "commission_amount_display",
        "balance_display",
        "image_tag",
    )
    list_filter = ["agency", "sim_card"]

    def image_tag(self, obj):
        if obj.screenshot:
            return mark_safe(
                f'<img src="{obj.screenshot.url}" width="100" height="100" style="object-fit: cover;"/>'
            )
        return "-"

    image_tag.short_description = "Capture transfert"

    def amount_display(self, obj):
        # formattage propre : 150 000 et devise dynamique
        amount = intcomma(obj.amount).replace(",", " ")
        currency = obj.currency  # ou obj.amount.currency.symbol
        return f"{amount} {currency}"

    amount_display.short_description = "Montant"

    def commission_amount_display(self, obj):
        # formattage propre : 150 000 et devise dynamique
        commission_amount = intcomma(obj.commission_amount).replace(",", " ")
        currency = obj.currency  # ou obj.amount.currency.symbol
        return f"{commission_amount} {currency}"

    commission_amount_display.short_description = "Commission"

    def balance_display(self, obj):
        # formattage propre : 150 000 et devise dynamique
        balance = intcomma(obj.balance).replace(",", " ")
        currency = obj.currency  # ou obj.amount.currency.symbol
        return f"{balance} {currency}"

    balance_display.short_description = "Solde"


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    list_display = ("agency", "amount", "transfer", "updated_at")
    list_filter = ["agency"]
