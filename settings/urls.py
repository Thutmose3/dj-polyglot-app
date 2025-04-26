from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path as url

from translation_api.api import PullTranslationsView
from translation_api.api import ReceiveTranslationsView
from translation_api.views import ai_translate
from translation_api.views import ai_translate_all_untranslated
from translation_api.views import homepage
from translation_api.views import TranslationListView
from translation_api.views import update_translation
from translation_api.views import update_translation_info_cell
from translation_api.views import update_validate_cell
from translation_api.views import validate

urlpatterns = [
    url(r"^jifowjqwieurtiwoutio27819qwfjko2pyt89ajigop273951243/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", homepage, name="homepage"),
    path(
        "translate/<str:language>/<int:source_project_id>", TranslationListView.as_view(), name="translation_dashboard"
    ),
    path("api/push-translations/", ReceiveTranslationsView.as_view(), name="receive_translations"),
    path("api/pull-translations/", PullTranslationsView.as_view(), name="pull_translations"),
    path(
        "update-translation/<str:language>/<int:translatable_string_id>", update_translation, name="update_translation"
    ),
    path("ai-translate/<str:language>/<int:translatable_string_id>/", ai_translate, name="ai_translate"),
    path("validate/<str:language>/<int:translatable_string_id>/", validate, name="validate"),
    path(
        "update-validate-cell/<str:language>/<int:translatable_string_id>/",
        update_validate_cell,
        name="update_validate_cell",
    ),
    path(
        "update-translation-info-cell/<str:language>/<int:translatable_string_id>/",
        update_translation_info_cell,
        name="update_translation_info_cell",
    ),
    path(
        "ai-translate-all-untranslated/<str:language>/<int:source_project_id>/",
        ai_translate_all_untranslated,
        name="ai_translate_all_untranslated",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
