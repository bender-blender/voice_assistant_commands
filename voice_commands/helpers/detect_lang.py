from lingua import Language, LanguageDetectorBuilder


def identify_the_language(text: str) -> str | None:
    languages = [Language.RUSSIAN, Language.ENGLISH]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()
    lang = detector.detect_language_of(text)
    if lang is not None:
        return lang.iso_code_639_1.name.lower()
    
    return None
