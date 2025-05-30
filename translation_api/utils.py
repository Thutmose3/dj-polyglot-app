def translate_string_deepl(string, target_lang, deepl_key, source_lang=None, context=None, formality="default"):
    import deepl

    translator = deepl.Translator(deepl_key)
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
