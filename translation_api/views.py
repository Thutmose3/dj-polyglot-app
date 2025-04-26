import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django_filters.views import FilterView
from django_tables2 import SingleTableView

from .filters import TranslatableStringFilter
from .models import SourceProject
from .models import TranslatableString
from .models import TranslatedString
from .tables import TranslatableStringTable
from .utils import translate_string_deepl

logger = logging.getLogger("django")


@login_required
@require_GET
def homepage(request):
    """Homepage."""
    return render(
        request,
        "homepage.html",
        context={
            "source_projects": SourceProject.objects.filter(users=request.user),
            "languages": [code for code, _ in settings.LANGUAGES],
        },
    )


class TranslationListView(FilterView, SingleTableView):
    """List view for translations."""

    table_class = TranslatableStringTable
    model = TranslatableString
    template_name = "translation_list.html"
    filterset_class = TranslatableStringFilter
    table_pagination = {"per_page": 50}

    def get_table_kwargs(self):
        """Return the keyword arguments for instantiating the table."""
        kwargs = super().get_table_kwargs()
        kwargs["language"] = self.kwargs["language"]
        return kwargs

    def get_filterset_kwargs(self, filterset_class):
        """Return the keyword arguments for instantiating the filterset."""
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["language"] = self.kwargs["language"]
        return kwargs

    def get_queryset(self):
        """Get only the not archived objects."""
        return super().get_queryset().filter(archived=False)

    def get_context_data(self, **kwargs):
        """Add the languages to the context."""
        context = super().get_context_data(**kwargs)
        language = self.kwargs.get("language")
        source_project_id = self.kwargs.get("source_project_id")

        source_project = SourceProject.objects.get(id=source_project_id)
        if not source_project.users.filter(id=self.request.user.id).exists():
            raise PermissionError("You are not allowed to view this project")

        total_translated_strings = TranslatedString.objects.filter(
            string__source_project=source_project, language=language
        ).count()

        context["language"] = language
        context["source_project"] = source_project
        context["total_translated_strings"] = total_translated_strings
        context["search_placeholder"] = "Search for translations"

        return context


@login_required
@require_POST
def update_translation(request, language, translatable_string_id):
    """Update cell."""

    record = TranslatableString.objects.get(id=translatable_string_id)

    if not record.source_project.users.filter(id=request.user.id).exists():
        raise PermissionError("You are not allowed to view this project")

    if not record.source_project.admins.filter(id=request.user.id).exists():
        raise PermissionError("You are not allowed to edit this project")

    translated_string_obj = TranslatedString.objects.update_or_create(
        string=record,
        language=language,
        defaults={
            "translated_string": request.POST["translated_string"],
            "translated_by": request.user,
            "translated_by_ai": False,
            "translated_at": timezone.now(),
        },
    )[0]

    translated_string_obj.validated = False
    translated_string_obj.validated_by = None
    translated_string_obj.validated_at = None
    translated_string_obj.save()

    messages.success(request, "Translation updated")
    response = HttpResponse(status=204)
    response.headers["HX-Trigger"] = {
        f"trigger_validated_cell_{language}_{translatable_string_id}": "",
        f"trigger_info_cell_{language}_{translatable_string_id}": "",
    }
    return response


@login_required
def ai_translate(request, language, translatable_string_id):
    """Update cell."""

    translatable_string = TranslatableString.objects.get(id=translatable_string_id)
    if not translatable_string.source_project.users.filter(id=request.user.id).exists():
        raise PermissionError("You are not allowed to view this project")

    if not translatable_string.source_project.admins.filter(id=request.user.id).exists():
        raise PermissionError("You are not allowed to edit this project")

    context = translatable_string.context
    if not context:
        context = translatable_string.source_project.default_context

    deepl_translated_string = translate_string_deepl(
        translatable_string.string, target_lang=language, source_lang="en", context=context
    )

    if translatable_string.string.count("{}") != deepl_translated_string.count("{}"):
        logger.error("String has different amount of curly brackets in source and target language")
        return JsonResponse({"error": "String has different amount of curly brackets in source and target language"})

    translated_string_obj = TranslatedString.objects.get_or_create(
        string=translatable_string,
        language=language,
    )[0]

    translated_string_obj.translated_string = deepl_translated_string
    translated_string_obj.translated_by = None
    translated_string_obj.translated_by_ai = True
    translated_string_obj.translated_at = timezone.now()
    translated_string_obj.validated = False
    translated_string_obj.validated_by = None
    translated_string_obj.validated_at = None
    translated_string_obj.save()

    messages.success(request, "Translation updated")
    response = render(
        request,
        "translation_cell.html",
        context={
            "translatable_string": translatable_string,
            "language": language,
            "translated_string": translated_string_obj,
        },
    )
    response.headers["HX-Trigger"] = {
        f"trigger_validated_cell_{language}_{translatable_string_id}": "",
        f"trigger_info_cell_{language}_{translatable_string_id}": "",
    }
    return response


@login_required
def ai_translate_all_untranslated(request, language, source_project_id):
    """Translate all strings."""
    source_project = get_object_or_404(SourceProject, id=source_project_id)
    translatable_strings = TranslatableString.objects.filter(source_project=source_project)
    if not source_project.users.filter(id=request.user.id).exists():
        raise PermissionError("You are not allowed to view this project")

    if not source_project.admins.filter(id=request.user.id).exists():
        raise PermissionError("You are not allowed to view this project")

    for translatable_string in translatable_strings:
        if (
            not translatable_string.translatedstring_set.filter(language=language)
            .exclude(translated_string="")
            .exists()
        ):
            context = translatable_string.context
            if not context:
                context = translatable_string.source_project.default_context
            translated_string = translate_string_deepl(
                translatable_string.string, target_lang=language, source_lang="en", context=context
            )

            # make sure the same amount of {} are in the translated string
            if translatable_string.string.count("{}") != translated_string.count("{}"):
                logger.error("String  has different amount of curly brackets in source and target language")
                continue

            translated_string_obj = TranslatedString.objects.get_or_create(
                string=translatable_string,
                language=language,
            )[0]

            translated_string_obj.translated_string = translated_string
            translated_string_obj.translated_by = None
            translated_string_obj.translated_by_ai = True
            translated_string_obj.save()

    messages.success(request, "All strings translated")
    return HttpResponseRedirect(reverse("translation_dashboard", args=[language, source_project_id]))


@login_required
def validate(request, language, translatable_string_id):
    """Update cell."""

    translatable_string = TranslatableString.objects.get(id=translatable_string_id)
    translated_string = get_object_or_404(
        TranslatedString,
        string=translatable_string,
        language=language,
    )

    if not translated_string.string.source_project.users.filter(id=request.user.id).exists():
        raise PermissionError("You are not allowed to view this project")

    if not translated_string.string.source_project.admins.filter(id=request.user.id).exists():
        raise PermissionError("You are not allowed to view this project")

    translated_string.validated = True
    translated_string.validated_by = request.user
    translated_string.validated_at = timezone.now()
    translated_string.save()
    messages.success(request, "Translation validated")
    response = render(
        request,
        "actions_cell.html",
        context={
            "translatable_string": translatable_string,
            "language": language,
            "translated_string": translated_string,
        },
    )

    response.headers["HX-Trigger"] = {
        f"trigger_validated_cell_{language}_{translatable_string_id}": "",
        f"trigger_info_cell_{language}_{translatable_string_id}": "",
    }

    return response


@login_required
def update_validate_cell(request, language, translatable_string_id):
    """Update cell."""

    translatable_string = TranslatableString.objects.get(id=translatable_string_id)

    translated_string = get_object_or_404(
        TranslatedString,
        string=translatable_string,
        language=language,
    )

    response = render(
        request,
        "actions_cell.html",
        context={
            "translatable_string": translatable_string,
            "language": language,
            "translated_string": translated_string,
        },
    )
    return response


@login_required
def update_translation_info_cell(request, language, translatable_string_id):
    """Update cell."""

    translatable_string = TranslatableString.objects.get(id=translatable_string_id)

    translated_string = get_object_or_404(
        TranslatedString,
        string=translatable_string,
        language=language,
    )

    response = render(
        request,
        "info_cell.html",
        context={
            "translatable_string": translatable_string,
            "language": language,
            "translated_string": translated_string,
        },
    )
    return response
