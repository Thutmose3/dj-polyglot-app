# flake8: noqa
from .base import *

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# ==============================================================================
# DATABASE
# ==============================================================================
if os.getenv("CI", None):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }
else:
    DB_NAME = config("DB_NAME", "")
    DB_PW = config("DB_PW", "")
    DB_USER = config("DB_USER", "")
    DB_HOST = config("DB_HOST", "")
    DB_PORT = config("DB_PORT", "")
    assert DB_NAME
    assert DB_PW
    assert DB_USER
    assert DB_HOST
    assert DB_PORT

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PW,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }
