from lemminflect import getAllInflections
from pymorphy3 import MorphAnalyzer


def all_forms_ru(word: str) -> str:
    analyzer = MorphAnalyzer()
    parsed = analyzer.parse(word)[0]
    return "|".join(sorted({form.word for form in parsed.lexeme})) + "|"


def all_forms_en(word: str) -> str:
    inflections = getAllInflections(word, upos='NOUN')
    return "|".join(sorted({forms[0] for forms in inflections.values()}))


def create_pattern(optional:bool = False,*args) -> str:
    parts = [arg for arg in args]
    inner = "|".join(parts)
    return f"({inner})? " if optional else f"({inner})"
