import django_filters
from django.db.models import Q

from .models import TranslatableString
from .models import TranslatedString


class TranslatableStringFilter(django_filters.FilterSet):
    """Filter Contact model."""

    validated = django_filters.BooleanFilter(method="filter_by_validated")
    translated = django_filters.BooleanFilter(method="filter_by_validated")
    search = django_filters.CharFilter(method="filter_by_search")

    class Meta:
        model = TranslatableString
        fields = ["source_project", "string", "search"]

    def __init__(self, *args, **kwargs):
        self.language = kwargs.pop("language")
        super().__init__(*args, **kwargs)

    def filter_by_validated(self, queryset, name, value):
        """Filter by validated."""
        if value is True:
            translatable_string_ids = TranslatedString.objects.filter(
                validated=True, language=self.language
            ).values_list("string", flat=True)
            return queryset.filter(id__in=translatable_string_ids).distinct()
        if value is False:
            translatable_string_ids = TranslatedString.objects.filter(
                validated=False, language=self.language
            ).values_list("string", flat=True)

            queryset = queryset.filter(id__in=translatable_string_ids)

            return queryset.distinct()
        return queryset.distinct()

    def filter_by_translated(self, queryset, name, value):
        """Filter by translated."""
        if value is True:
            translatable_string_ids = TranslatedString.objects.filter(
                string__isnull=False, language=self.language
            ).values_list("string", flat=True)
            return queryset.filter(id__in=translatable_string_ids).distinct()
        if value is False:
            translatable_string_ids = TranslatedString.objects.filter(
                string__isnull=True, language=self.language
            ).values_list("string", flat=True)
            return queryset.filter(id__in=translatable_string_ids).distinct()
        return

    def filter_by_search(self, queryset, name, value):
        """Filter by search."""
        translatable_string_ids = TranslatedString.objects.filter(
            translated_string__icontains=value, language=self.language
        ).values_list("string", flat=True)

        return queryset.filter(
            Q(id__in=translatable_string_ids) | Q(string__icontains=value) | Q(context__icontains=value)
        ).distinct()
