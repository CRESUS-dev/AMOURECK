from .base import *

DEBUG = False
ENVIRONMENT = "STAGING"

ALLOWED_HOSTS = [
    "staging.amoureck.com",
    "127.0.0.1",
    "izisoft.org",
    "www.izisoft.org",
    "admin.izisoft.org",
]

DATABASES = {
    "default": {
        "ENGINE": config("SQL_ENGINE", default="django.db.backends.postgresql").strip(),
        "NAME": config("SQL_DATABASE"),
        "USER": config("SQL_USER"),
        "PASSWORD": config("SQL_PASSWORD"),
        "HOST": config("SQL_HOST", default="localhost"),
        "PORT": config("SQL_PORT", default="5432"),
    }
}
