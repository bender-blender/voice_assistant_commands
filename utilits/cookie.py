from typing import Any, Callable


def cookie[T: Any](phrase: str, parser: Callable[[str], T | None]) -> tuple[str, T] | None:
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
