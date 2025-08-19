from typing import Any, Callable, Optional, Tuple, TypeVar

T = TypeVar("T")  # Объявляем TypeVar

def cookie(phrase: str, parser: Callable[[str], Optional[T]]) -> Optional[Tuple[str, T]]:
    """For dirty providers only"""
    value = parser(phrase)

    # Optimisations:
    # - binary search
    # - parallel processing?

    # try remove from left side
    while True:
        new_phrase = " ".join(phrase.split(" ")[1:])
        new_value = parser(new_phrase)
        if new_value == value:
            phrase = new_phrase
            value = new_value
            continue
        else:
            break

    # try remove from right side
    while True:
        new_phrase = " ".join(phrase.split(" ")[:-1])
        new_value = parser(new_phrase)
        if new_value == value:
            phrase = new_phrase
            value = new_value
            continue
        else:
            break

    if value is None:
        return None
    return (phrase, value)
