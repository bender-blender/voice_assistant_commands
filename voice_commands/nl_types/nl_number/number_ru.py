from rus2num import Rus2Num

from stark.core.parsing import Object, Pattern, ParseError
from stark.core.types.object import classproperty

from voice_commands.nl_types.parsing_context import pattern_parser


class NLNumberRU(Object):
    value: float
    is_ordinal: bool
    ru = Rus2Num()

    @classproperty
    def pattern(cls):
        return Pattern("**")

    async def did_parse(self, from_string):

        new_text, spans = self.ru.parse_with_spans(
            from_string
        )

        if not spans:
            raise ParseError("Число не найдено")

        first = spans[0]
        sub = str(first["substring"])
        is_negative = "минус" in from_string.lower().split()

        if is_negative and not sub.startswith("минус"):
            sub = f"минус {sub}"

        if len(spans) >= 2:

            try:
                self.value = float(
                    f"{spans[0]["parsed"]}.{spans[1]["parsed"]}")

            except ValueError:
                raise ParseError(
                    "Не удалось разобрать число"
                )

            if is_negative:
                self.value = -abs(self.value)

            self.is_ordinal = False

            return from_string[spans[0]["start"]:spans[1]["stop"]]

        try:
            self.value = float(first["parsed"])

        except ValueError:
            parts = first["parsed"].split()
            if len(parts) != 2:
                raise ParseError(
                    f"Некорректное число: {first['parsed']}"
                )

            numerator = float(parts[0])
            denominator = float(parts[1])

            if denominator == 0:
                raise ParseError(
                    "Знаменатель не может быть равен нулю"
                )

            self.value = numerator / denominator

        if is_negative:
            self.value = -abs(self.value)

        self.is_ordinal = sub.endswith(("ый", "ий", "ой"))
        return sub


pattern_parser.register_parameter_type(NLNumberRU)
