# flake8: noqa
from .base import *

# ==============================================================================
# CORE SETTINGS
# ==============================================================================
INSTALLED_APPS += [
    "django_browser_reload",
    "django_extensions"
]

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media")
MEDIA_URL = "/media/"
