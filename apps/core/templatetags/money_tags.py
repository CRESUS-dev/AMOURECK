from django import template
from django.utils.formats import number_format
from django.conf import settings
from apps.country.models import Country


register = template.Library()


def money(value, request=None):
    """
    Formatte un montant avec la devise du pays stocké dans la session.
    Utilisation : {{ montant|money:request }}
    """
    if value is None:
        return ""

        # Valeur par défaut
    default_currency = getattr(settings, "DEFAULT_CURRENCY", "")

    currency = default_currency

    # Récupérer le code pays depuis la session
    country_code = None
    if request and hasattr(request, "session"):
        country_code = request.session.get("iso_code")

    # Si on a un code pays, récupérer la devise depuis la base
    if country_code:
        try:
            country = Country.objects.get(iso_code=country_code)
            currency = country.currency
        except Country.DoesNotExist:
            currency = default_currency

    # Formatage du nombre (ex: 1 234,56)
    formatted_value = number_format(value, 2, decimal_sep=",", thousand_sep=" ")

    return f"{formatted_value} {currency}"
