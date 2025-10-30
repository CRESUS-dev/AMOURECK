import json
import os
from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def vite_static(entry_name):
    """
    Retourne le chemin statique du fichier Vite selon manifest.json
    """
    # 🔧 Nouveau chemin absolu vers le manifest
    manifest_path = os.path.join(settings.BASE_DIR, "static", "vite", "manifest.json")

    if not os.path.exists(manifest_path):
        # fallback : fichier non encore généré
        print(f"[vite_static] manifest non trouvé: {manifest_path}")
        return static(f"vite/{entry_name}")

    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except Exception as e:
        print("[vite_static] Erreur de lecture manifest:", e)
        return static(f"vite/{entry_name}")

    file_info = manifest.get(entry_name)
    if not file_info:
        print(f"[vite_static] entrée '{entry_name}' non trouvée dans manifest")
        return static(f"vite/{entry_name}")

    final_path = static(f"vite/{file_info['file']}")
    print(f"[vite_static] Fichier injecté: {final_path}")
    return final_path
