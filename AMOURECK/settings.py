import os
import sys
from pathlib import Path
from django.urls import reverse_lazy
from django.contrib.messages import constants as messages
import posixpath
from decouple import config, Csv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings.old - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config("DEBUG", default=False, cast=bool)
DEBUG = config('DEBUG')
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', cast=Csv() )

CSRF_TRUSTED_ORIGINS = config("DJANGO_CSRF_TRUSTED_ORIGINS",cast=Csv())

DATABASES = {
    'default': {
        'ENGINE': config('SQL_ENGINE', default='django.db.backends.postgresql').strip(),
        'NAME': config('SQL_DATABASE'),
        'USER': config('SQL_USER'),
        'PASSWORD': config('SQL_PASSWORD'),
        'HOST': config('SQL_HOST', default='localhost'),
        'PORT': config('SQL_PORT', default='5432'),
    }
}


# Application definition

INSTALLED_APPS = [
    # "jazzmin",
    "crispy_forms",
    "crispy_bootstrap5",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.dashboard",
    "apps.accounts",
    "apps.core",
    "apps.country",
    "apps.customer",
    "apps.passengers",
    "simple_history",
    'django_select2',
    "apps.package",
    "apps.chat",
    "django_extensions",
    "channels",


]

# Dev: mémoire (suffisant en local)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}



ASGI_APPLICATION = "AMOURECK.asgi.application"

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "apps.core.middleware.current_request.CurrentRequestMiddleware"
]

ROOT_URLCONF = "AMOURECK.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']  # globals templates
        ,
        "APP_DIRS": True,  # apps templates
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.user_context",
                "apps.core.context_processors.enterprise_context",
            ],
        },
    },
]

WSGI_APPLICATION = "AMOURECK.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = 'accounts.CustomUser'

JAZZMIN_SETTINGS = {
    "site_title": "Administration AMOURECK",
    "site_header": "Admin AMOURECK",
    "site_brand": "AMOURECK",
    "welcome_sign": "Administration AMOURECK",
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "myapp": "fas fa-boxes",
    },
}

# os.getenvuration des messages d'erreur
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic en prod
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = reverse_lazy('dashboard')
LOGOUT_REDIRECT_URL = '/login/'

# Media files (users uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings.old
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT')
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE')
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE')
SECURE_HSTS_SECONDS = os.getenv('SECURE_HSTS_SECONDS')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    "127.0.0.1"
]

CURRENCY_CHOICES = [
    ('XOF', 'Franc CFA BCEAO'),
    ('GNF', 'Franc Guinéen'),
    ('USD', 'Dollar Américain'),
    ('EUR', 'Euro'),
]

DEFAULT_CURRENCY = 'XOF'
