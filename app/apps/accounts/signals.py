from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from .models import LoginHistory


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    # Créer une nouvelle entrée à la connexion
    LoginHistory.objects.create(user=user, ip_address=ip, user_agent=user_agent)


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    # Chercher la dernière session ouverte pour l'utilisateur
    try:
        last_login = LoginHistory.objects.filter(user=user, logout_time__isnull=True).latest('login_time')
        last_login.logout_time = now()
        last_login.save()
    except LoginHistory.DoesNotExist:
        pass  # Aucun login ouvert, rien à faire


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
