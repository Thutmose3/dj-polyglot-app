import os

from decouple import config
from decouple import Csv

# ==============================================================================
# CORE SETTINGS
# ==============================================================================
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SECRET_KEY = config("SECRET_KEY")

THOUSAND_SEPARATOR = False

WSGI_APPLICATION = "settings.wsgi.application"

INTERNAL_IPS = config("INTERNAL_IPS", default="127.0.0.1,localhost", cast=Csv())
CORS_ORIGIN_WHITELIST = []

ROOT_URLCONF = "settings.urls"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "compressor",
    "template_partials",
    "crispy_forms",
    "crispy_tailwind",
    "django_tables2",
    "allauth_ui",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "widget_tweaks",
    "slippers",
]

PROJECT_APPS = [
    "translation_api",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

LANGUAGES = [
    ("en", "English"),
    ("fr", "Français"),
    ("de", "Deutsch"),
    ("es", "Español"),
    ("nl", "Nederlands"),
    ("it", "Italiano"),
    ("pt-pt", "Português"),
    ("bg", "Български"),
    ("cs", "Čeština"),
    ("da", "Dansk"),
    ("el", "Ελληνικά"),
    ("et", "Eesti"),
    ("lv", "Latviešu"),
    ("fi", "Suomi"),
    ("hu", "Magyar"),
    ("no", "Norsk"),
    ("pl", "Polski"),
    ("ro", "Română"),
    ("ru", "Русский"),
    ("sk", "Slovenčina"),
    ("sl", "Slovenščina"),
    ("sv", "Svenska"),
    ("tr", "Türkçe"),
    ("ar", "العربية"),
    ("zh-hans", "中文 (简体)"),
    ("zh-hant", "中文 (繁體)"),
    ("ja", "日本語"),
    ("ko", "한국어"),
    ("uk", "Українська"),
]

# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "translation_api.middleware.HtmxMessageMiddleware",
]

# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

default_loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]
cached_loaders = [("django.template.loaders.cached.Loader", default_loaders)]
partial_loaders = [("template_partials.loader.Loader", cached_loaders)]

DJANGO_TABLES2_TEMPLATE = "django_tables2/flowbite_table.html"
DJANGO_TABLES2_PAGE_LENGTH = 25

DJANGO_TABLES2_TABLE_ATTRS = {
    "th": {
        "class": "px-1 py-2 whitespace-nowrap text-xs font-medium text-left text-gray-500 uppercase dark:text-gray-400",
    },
    "td": {
        "class": "px-1 py-2 font-medium text-gray-900 dark:text-white",
    },
    "thead": {
        "class": "px-1 py-2 text-xs font-medium text-left text-gray-500 uppercase dark:text-gray-400",
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": partial_loaders,
            "builtins": [
                "django.templatetags.static",
                "django.templatetags.l10n",
                "django.templatetags.i18n",
                "slippers.templatetags.slippers",
            ],
        },
    },
]

# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================
STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SESSION_COOKIE_AGE = 31536000  # 1 year
SITE_ID = 1

# ==============================================================================
# DATABASE
# ==============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "dj_polyglot_app",
        "USER": "debug",
        "PASSWORD": "debug",
        "HOST": "postgres",
        "PORT": "5432",
    }
}

# ==============================================================================
# Django Allauth Settings
# ==============================================================================
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_GET = True
SESSION_COOKIE_AGE = 7776000  # 90 days
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False

# ==============================================================================
# REST FRAMEWORK SETTINGS
# ==============================================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

DEEPL_KEY = config("DEEPL_KEY")

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

base_input = "bg-gray-50 border text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

CRISPY_TAILWIND_STYLE = {
    "text": base_input,
    "number": base_input,
    "email": base_input,
    "url": base_input,
    "password": base_input,
    "textarea": base_input,
    "date": base_input,
    "datetime": base_input,
    "time": base_input,
    "checkbox": "w-4 h-4 bg-gray-50 rounded border-gray-300 focus:ring-3 focus:ring-primary-300 dark:focus:ring-primary-600 dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600",
    "checkboxselectmultiple": "w-4 h-4 bg-gray-50 rounded border-gray-300 focus:ring-3 focus:ring-primary-300 dark:focus:ring-primary-600 dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600",
    "select": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
}

ALLAUTH_UI_THEME = "business"
