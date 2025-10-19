from django.contrib import admin
from .models import Room, Message
from django.utils.html import format_html


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    fields = ['name', 'user']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'value', 'room', 'image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;"/>', obj.image.url)
        return "_"
    image_tag.short_description = "image"




