from django.apps import AppConfig


class TranslationApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "translation_api"

    def ready(self):
        import translation_api.signals  # noqa
