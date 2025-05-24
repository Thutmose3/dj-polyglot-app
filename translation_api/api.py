import logging

from django.conf import settings
from django.db.models import Prefetch
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SourceProject
from .models import TranslatableString
from .models import TranslatedString
from .utils import translate_string_deepl

logger = logging.getLogger("django")


class ReceiveTranslationsView(APIView):
    """Receive translations from the client and save them to the database."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Receive translations from the client and save them to the database."""
        translations = request.data.get("translations", [])
        no_obselete = request.data.get("no_obselete", False)
        source_project = SourceProject.objects.get_or_create(
            name=request.data.get("source_project"), admins__in=[request.user]
        )[0]

        translatable_string_ids = []

        for translation in translations:
            msgid = translation.get("msgid")
            context = translation.get("context")
            # locale = translation.get("locale")
            translatable_string, created = TranslatableString.objects.get_or_create(
                string=msgid, source_project=source_project, context=context
            )
            translatable_string_ids.append(translatable_string.id)
            for language in [code for code, _ in settings.LANGUAGES]:
                if language == "en":
                    continue

                if created:
                    if not context:
                        context = source_project.default_context

                    translated_string = translate_string_deepl(
                        translatable_string.string, target_lang=language, source_lang="en", context=context
                    )
                    # make sure the same amount of {} are in the translated string
                    if translatable_string.string.count("{}") != translated_string.count("{}"):
                        logger.error("String has different amount of curly brackets in source and target language")
                        continue

                    TranslatedString.objects.create(
                        string=translatable_string,
                        language=language,
                        translated_string=translated_string,
                        translated_by_ai=True,
                        translated_by=None,
                    )

        if no_obselete:
            TranslatableString.objects.filter(source_project=source_project).exclude(
                id__in=translatable_string_ids
            ).delete()

        return Response({"message": "Translations received successfully"}, status=status.HTTP_200_OK)


class PullTranslationsView(APIView):
    """Send translations to the client."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Send translations to the client."""
        translations = []
        source_projects = request.data.get("source_project").split(",")

        # Prefetch translated strings for all languages except English
        translatable_strings = TranslatableString.objects.filter(
            source_project__name__in=source_projects
        ).prefetch_related(
            Prefetch(
                "translatedstring_set",
                queryset=TranslatedString.objects.exclude(language="en"),
                to_attr="translations",
            )
        )

        # Loop over each translatable string
        for translatable_string in translatable_strings:
            # Loop over each translated string related to the translatable string
            for translated_string in translatable_string.translations:
                if translated_string.string.source_project.name in source_projects:
                    translations.append(
                        {
                            "msgid": translatable_string.string,
                            "msgstr": translated_string.translated_string,
                            "msgctxt": translatable_string.context,
                            "locale": translated_string.language,
                        }
                    )

        return JsonResponse({"translations": translations})
