from django.apps import AppConfig


class TransfertsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.transferts"

    # def ready(self):
    #     import apps.transferts.signals
