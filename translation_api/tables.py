import html

import django_tables2 as tables
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .models import TranslatableString


class TranslatableStringTable(tables.Table):

    translation = tables.Column(
        verbose_name="Translation",
        orderable=False,
        empty_values=(),
    )
    info = tables.Column(
        verbose_name="Info",
        orderable=False,
        empty_values=(),
    )

    actions = tables.Column(
        verbose_name="Actions",
        orderable=False,
        empty_values=(),
    )

    class Meta:
        model = TranslatableString
        fields = [
            "string",
            "translation",
            "context",
            "actions",
            "info",
        ]

    def __init__(self, language, *args, **kwargs):
        self.language = language
        super().__init__(*args, **kwargs)

        self.row_attrs = {
            "class": lambda record: (
                "border-b bg-green-500 hover:bg-green-600 cursor-pointer"
                if self._get_translated_string_cached(record).validated
                else (
                    "border-b bg-sky-500 hover:bg-sky-500 dark:hover:border-green-600 cursor-pointer"
                    if self._get_translated_string_cached(record).translated_by_ai
                    else "border-b bg-pink-300 border-pink-300 hover:bg-pink-400 "
                    "dark:border-pink-600 dark:bg-pink-700 dark:hover:bg-pink-600 "
                    "dark:hover:border-pink-600 cursor-pointer"
                )
            )
        }

    def render_string(self, value):
        escaped = html.escape(value)
        return mark_safe(escaped.replace("\n", "<br>"))

    def render_translation(self, record):
        return render_to_string(
            "translation_cell.html",
            {
                "translatable_string": record,
                "language": self.language,
                "translated_string": self._get_translated_string_cached(record),
            },
        )

    def render_info(self, record):
        return render_to_string(
            "info_cell.html",
            {
                "translatable_string": record,
                "language": self.language,
                "translated_string": self._get_translated_string_cached(record),
            },
        )

    def render_actions(self, record):
        return render_to_string(
            "actions_cell.html",
            {
                "translatable_string": record,
                "language": self.language,
                "translated_string": self._get_translated_string_cached(record),
            },
        )

    def _get_translated_string_cached(self, record):
        if not hasattr(record, "_translated_string_cache"):
            record._translated_string_cache = record.get_translated_string(language=self.language)
        return record._translated_string_cache
