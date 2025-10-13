from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import CustomUser
from simple_history.models import HistoricalRecords
from django.utils import timezone
import os
from datetime import datetime


class Room(TimeStampedModel):
    name = models.CharField(max_length=2000)
    history = HistoricalRecords()


def chat_media_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    base = os.path.splitext(filename)[0]  # nom sans extension
    filename = f"{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return f"uploads/{datetime.now().strftime('%Y/%m/%d')}/{filename}"


class Message(TimeStampedModel):
    value = models.CharField(max_length=1000000)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, null=False)
    image = models.ImageField(upload_to='chat_media_directory_path', blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        if self.value:
            return f"{self.user} → {self.value[:20]}"
        return f"{self.user} → [image]"
