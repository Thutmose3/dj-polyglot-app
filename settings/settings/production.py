# flake8: noqa
from .base import *

DEBUG = False

# ==============================================================================
# DATABASE
# ==============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME", ""),
        "USER": config("DB_USER", ""),
        "PASSWORD": config("DB_PW", ""),
        "HOST": config("DB_HOST", ""),
        "PORT": config("DB_PORT", ""),
    }
}

# ==============================================================================
# LOGGING
# ==============================================================================
BETTERSTACK_TOKEN = config("BETTERSTACK_TOKEN", "")

if BETTERSTACK_TOKEN:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "logtail": {
                "class": "logtail.LogtailHandler",
                "source_token": BETTERSTACK_TOKEN,
                "host": config("BETTERSTACK_HOST"),
            },
        },
        "loggers": {
            "": {
                "handlers": [
                    "logtail",
                ],
                "level": "INFO",
            },
        },
    }


# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1000000
SECURE_FRAME_DENY = True
