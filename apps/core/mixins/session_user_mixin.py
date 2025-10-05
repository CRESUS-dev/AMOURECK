# core/mixins/session_user_mixin.py
from django.conf import settings
from django.db import models
from apps.core.middleware.current_request import get_current_request

class SessionUserMixin(models.Model):
    """Mixin pour associer automatiquement un user et des infos de session à un modèle."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    agency_id = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True  # Ne crée pas de table dans la BD

    def save(self, *args, **kwargs):
        request = get_current_request()
        if request:
            if hasattr(request, "user") and request.user.is_authenticated:
                self.user = request.user
            if request.session.get("agency_id"):
                self.agency_id = request.session["agency_id"]
        super().save(*args, **kwargs)
