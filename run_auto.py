import os
import socket
from django.core.management import execute_from_command_line


def get_local_ip():
    """
    Récupère l'adresse IP locale valide.
    Fonctionne pour Wi-Fi, Ethernet, Hotspot.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connexion "factice" pour forcer le choix de l'interface réseau
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AMOURECK.settings")

    ip = get_local_ip()
    port = "8000"

    print(f"\n🌐 Django disponible sur : http://{ip}:{port}\n")
    print("⚡ Ouvre cette URL depuis ton téléphone (connecté au même réseau)")

    execute_from_command_line(["manage.py", "runserver", f"{ip}:{port}"])
