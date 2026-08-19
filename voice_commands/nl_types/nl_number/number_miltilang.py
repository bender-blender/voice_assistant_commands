from number_parser import parse, parse_ordinal, parse_number


from voice_commands.nl_types.parsing_context import pattern_parser
from stark.general.localisation import LocaleString
from stark.general.classproperty import classproperty
from stark.core.parsing import Pattern, ParseError
from stark.core.types import Object


class NLMultiNumber(Object):

    value: float
    is_ordinal: bool

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    @classmethod
    def check_type(cls, words: list[str] | tuple[str] | str, from_string: str):
        if type(words) in (list, tuple):
            check_words = any([i for i in from_string.split() if i in words])
        if type(words) == str:
            check_words = any([i for i in from_string.split() if i == words])

        return check_words if check_words else None

    def get_fraction(self, words: list[str] | tuple[str] | str, from_string: str):

        check_words = self.check_type(words, from_string)

        if check_words:
            part = [i if i in words else parse_number(
                i) for i in from_string.split() if i in words or parse_number(i)]
            sub = [str(i) for i in from_string.split()
                   if i in words or parse_number(i)]
            for index, value in enumerate(part):
                if type(value) == LocaleString:
                    part[index] = "."

            if "minus" in from_string:
                sub.insert(0, "minus")

            fraction = float("".join([str(i) for i in part]))
            return fraction, " ".join(sub) if "minus" not in from_string else -fraction, " ".join(sub)

        return None

    def get_parts(self, settings: dict[tuple[str], float], from_string: str):
        words = from_string.split()
        num_sub = [word for word in words if parse_number(word)]
        sub_part = [word for group in settings.keys()
                    for word in group if word in words]
        check_words = self.check_type(sub_part, from_string)

        if not check_words:
            return None

        part = [value for names, value in settings.items() if any(word in names for word in words)]

        if len(num_sub) == 0 and len(sub_part) == 1:
            return part[0] , " ".join(sub_part)

        final_sub = words[words.index(num_sub[0]):words.index(sub_part[0])+1]
        
        value = float(parse_number("".join(num_sub)))
        if "minus" in from_string:
            value = -value
            final_sub.insert(0, "minus")
        
        if "and" in final_sub:
            return value + part[0], " ".join(final_sub)

        return value * part[0], " ".join(final_sub)
        

    def get_ordinary_number(self, from_string: str):
        words = []
        

        for word in from_string.split():
            parsed = parse_number(word) or parse_ordinal(word)
            if parsed is not None:
                words.append(word)

        if not words:
            return None

        print(from_string)
        value = float(parse(" ".join(words)))
        if "minus" in from_string:
            value = -value
            words.insert(0, "minus")

        return value, " ".join(words)


    async def did_parse(self, from_string: LocaleString) -> str:
        part = self.get_parts({
            ("half","halfs"):0.5,
            ("quarter","quarters"):1/4,
            ("third"):1/3},
            from_string)

        if part:
            self.value = part[0]
            self.is_ordinal = False
            return part[1]


        fraction = self.get_fraction(["point", "points", "and"], from_string)
        if fraction:
            self.value = fraction[0]
            self.is_ordinal = False
            return fraction[1]


        ordinary_number = self.get_ordinary_number(from_string)
        if ordinary_number:
            self.value = ordinary_number[0]
            self.is_ordinal = False if not ordinary_number[1].endswith(("st","th","nd","rd")) else True
            return ordinary_number[1]

        raise ParseError("number not found")

pattern_parser.register_parameter_type(NLMultiNumber)
