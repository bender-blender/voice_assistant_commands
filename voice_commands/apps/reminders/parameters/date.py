from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from .data_dictionary import GeneralDictionary
from dataclasses import dataclass


@dataclass
class Day(Object):

    day: String

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern(f'$day:String')

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

        self.day = " ".join([str(day)] + unknown_words) if day > 0 else " ".join(unknown_words)
        if not self.day:
            raise ParseError("Error parsing day: no valid words found")
        return self.day

Pattern.add_parameter_type(Day)
