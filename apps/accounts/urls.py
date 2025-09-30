from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=True)), # redirection sur la page de login
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),


]