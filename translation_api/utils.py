from django.conf import settings


def translate_string_deepl(string, target_lang, source_lang=None, context=None, formality="default"):
    """Translate a string using depl."""
    import deepl

    translator = deepl.Translator(settings.DEEPL_KEY)
    if target_lang == "no":
        target_lang = "nb"
    if target_lang == "en":
        target_lang = "en-US"
    if not string:
        return ""
    result = translator.translate_text(
        string, target_lang=target_lang, source_lang=source_lang, context=context, formality=formality
    )
    return result.text
