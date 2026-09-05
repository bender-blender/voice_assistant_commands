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
        known_words = []
        index = 0

        dictionary = GeneralDictionary().words_to_numbers

        while index < len(words):
            word = words[index]
            if word in dictionary:
                if index + 1 < len(words) and words[index + 1] in dictionary:
                    day += dictionary[word] + dictionary[words[index + 1]]
                    index += 1
                else:
                    day += dictionary[word]
            else:
                known_words.append(word)
            index += 1

        if not day and not known_words:
            raise ParseError("Error parsing day: no valid words found")
        
        result = " ".join([str(day)] + known_words)


        self.value = result
        return from_string


Pattern.add_parameter_type(Day)
