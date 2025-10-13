# apps/chat/urls.py
from django.urls import path
from apps.chat import views


urlpatterns = [
    path("", views.home, name="home"),
    path("checkview/", views.checkview, name="checkview"),          # ✅ spécifique
    path("getMessages/<str:room>/", views.getMessages, name="getMessages"),  # ✅ spécifique
    path("<str:room>/", views.room, name="room"),                   # ⚠️ générique à la fin
]