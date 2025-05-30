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

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        translations = request.data.get("translations", [])
        no_obsolete = request.data.get("no_obsolete", False)
        source_project = SourceProject.objects.get_or_create(
            name=request.data.get("source_project"), admins__in=[request.user]
        )[0]

        translatable_string_ids = []

        for translation in translations:
            msgid = translation.get("msgid")
            context = translation.get("context")
            # locale = translation.get("locale")
            try:
                translatable_string, created = TranslatableString.objects.get_or_create(
                    string=msgid, source_project=source_project, context=context
                )

            except TranslatableString.MultipleObjectsReturned:
                return Response(
                    {
                        "error": f"Multiple translatable strings found for the same msgid and context: {msgid} with context: {context} in project {source_project.name}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            translatable_string_ids.append(translatable_string.id)
            for language in [code for code, _ in settings.LANGUAGES]:
                if language == "en":
                    continue

                if created:
                    if not context:
                        context = source_project.default_context

                    translated_string = translate_string_deepl(
                        translatable_string.string,
                        target_lang=language,
                        deepl_key=source_project.deepl_key,
                        source_lang="en",
                        context=context,
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

        if no_obsolete:
            TranslatableString.objects.filter(source_project=source_project).exclude(
                id__in=translatable_string_ids
            ).delete()

        return Response({"message": "Translations received successfully"}, status=status.HTTP_200_OK)


class PullTranslationsView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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
