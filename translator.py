from googletrans import Translator

translator = Translator()


def translate_line(line, src_lang, target_lang):
    if not line or not line.strip():
        return line

    try:
        result = translator.translate(line, src=src_lang, dest=target_lang)
        return result.text
    except Exception:
        return line


def translate_subtitle_text(text, src_lang, target_lang):
    if not text:
        return text

    lines = text.splitlines()
    translated = []

    for line in lines:
        translated.append(translate_line(line, src_lang, target_lang))

    return "\n".join(translated)
