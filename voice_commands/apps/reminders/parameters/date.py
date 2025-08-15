from dataclasses import dataclass

from stark.core.patterns import Pattern
from stark.core.types.object import Object, ParseError
from stark.general.classproperty import classproperty

from .data_dictionary import GeneralDictionary


@dataclass
class Day(Object):
    value: str

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    async def did_parse(self, from_string) -> str:
        words = from_string.strip().lower().split()
        day = 0
        unknown_words = []
        i = 0

        dictionary = GeneralDictionary().words_to_numbers

        while i < len(words):
            word = words[i]
            if word in dictionary:
                if i + 1 < len(words) and words[i + 1] in dictionary:
                    day += dictionary[word] + dictionary[words[i + 1]]
                    i += 1
                else:
                    day += dictionary[word]
            else:
                unknown_words.append(word)
            i += 1

        result = " ".join([str(day)] + unknown_words) if day > 0 else " ".join(unknown_words)

        if not result:
            raise ParseError("Error parsing day: no valid words found")

        self.value = result
        return from_string


Pattern.add_parameter_type(Day)
