from django.db import models
from django.utils import timezone
import os
from datetime import datetime

# from django.contrib.auth.models import User
from django.conf import settings


class TimeStampedModel(models.Model):
    """abstract class which add creation and modification date to any model"""

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NamedModel(models.Model):
    """Give a human readable name to models as primary identifier"""

    name = models.CharField(max_length=255, unique=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name


def media_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    base = os.path.splitext(filename)[0]  # nom sans extension
    filename = f"{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return f"uploads/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class Enterprise(TimeStampedModel):
    Name = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="Dénomination"
    )
    Address = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="Addresse"
    )
    Phone = models.CharField(max_length=20, verbose_name="N° Tél:")
    Head_office = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="Siège social"
    )
    logo = models.FileField(upload_to=media_directory_path, blank=True, null=True)

    def __str__(self):
        return self.Name


class Currency(NamedModel):
    code = models.CharField(max_length=5, null=False, blank=False)

    def __str__(self):
        return self.code
