from django.contrib import admin

from .models import SourceProject
from .models import TranslatableString
from .models import TranslatedString


@admin.register(TranslatableString)
class TranslatableStringAdmin(admin.ModelAdmin):
    search_fields = ["string", "context"]
    list_display = ["string", "source_project", "context"]
    list_filter = ["source_project"]


@admin.register(SourceProject)
class SourceProjectAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "default_context"]


@admin.register(TranslatedString)
class TranslatedStringAdmin(admin.ModelAdmin):
    search_fields = ["translated_string"]
    list_display = ["string", "language", "translated_string"]
    list_filter = ["language", "string__source_project", "validated", "translated_by_ai"]
