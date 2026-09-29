from rus2num.main import Rus2Num

from stark.core.parsing import Pattern, ParseError
from stark.general.classproperty import classproperty
from stark.core.types import Object

from voice_commands.nl_types.parsing_context import pattern_parser


class NLNumberRU(Object):
    value: float
    is_ordinal: bool

    locale = "ru_RU"

    SCALES = {
        "тысяча": 1_000,
        "тысячи": 1_000,
        "тысяч": 1_000,

        "миллион": 1_000_000,
        "миллиона": 1_000_000,
        "миллионов": 1_000_000,

        "миллиард": 1_000_000_000,
        "миллиарда": 1_000_000_000,
        "миллиардов": 1_000_000_000,
    }

    def __init__(self):
        self.parser = Rus2Num()

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    def is_free_digit(self, a, b):
        while a or b:
            if a % 10 and b % 10:
                return False

            a //= 10
            b //= 10

        return True

    def is_ordinal_word(self, word: str) -> bool:
        return (
            word.endswith(("ый", "ий", "ой"))
            and word not in self.parser.fractions
        )

    async def did_parse(self, from_string):
        numerator = None
        buffer = None
        parts = []

        integer_part = None
        decimal_point = False

        is_negative = False
        leading_zeros = 0

        total = 0

        parsed_words = []
        first_number_words = None

        self.is_ordinal = False

        def apply_sign(value):
            return -value if is_negative else value

        def decimal_value():
            if buffer is None:
                return integer_part

            digits = leading_zeros + (
                len(str(abs(buffer)))
                if buffer != 0
                else 0
            )

            if digits == 0:
                return integer_part

            return (
                integer_part
                + buffer / 10 ** digits
            )

        for word in str(from_string).lower().split():

            # Negative number
            if (
                word == "минус"
                and buffer is None
                and integer_part is None
                and total == 0
            ):
                is_negative = True
                parsed_words.append(word)
                continue

            # Decimal separators
            if word in (
                "целых",
                "целая",
                "точка",
                "точки",
            ):
                if buffer is None:
                    continue

                current = (
                    buffer
                    if numerator is None
                    else numerator
                )

                integer_part = total + current
                total = 0

                decimal_point = word in (
                    "точка",
                    "точки",
                )

                numerator = None
                buffer = None
                parts = []
                leading_zeros = 0
                first_number_words = None

                self.is_ordinal = False

                parsed_words.append(word)
                continue

            # Thousand / million / billion
            if word in self.SCALES:
                scale = self.SCALES[word]

                if numerator is not None:
                    group = numerator
                elif buffer is not None:
                    group = buffer
                else:
                    group = 1

                total += group * scale

                numerator = None
                buffer = None
                parts = []
                first_number_words = None

                self.is_ordinal = False

                parsed_words.append(word)
                continue

            is_fraction = word in self.parser.fractions

            try:
                if word in ("полтора", "полторы"):
                    number = 1.5

                else:
                    number = (
                        self.parser.fractions[word]
                        if is_fraction
                        else int(self.parser(word))
                    )

            except (ValueError, TypeError):

                if buffer is not None:
                    if (
                        integer_part is not None
                        and decimal_point
                    ):
                        self.value = apply_sign(
                            decimal_value()
                        )

                        self.is_ordinal = False

                        return " ".join(parsed_words)

                    current = (
                        buffer
                        if numerator is None
                        else numerator
                    )

                    self.value = apply_sign(
                        total + current
                    )

                    if (
                        numerator is not None
                        and first_number_words
                    ):
                        return " ".join(
                            first_number_words
                        )

                    return " ".join(parsed_words)

                if integer_part is not None:
                    self.value = apply_sign(
                        integer_part
                    )

                    return " ".join(parsed_words)

                if total:
                    self.value = apply_sign(total)

                    return " ".join(parsed_words)

                continue

            parsed_words.append(word)

            # Ordinal
            if not is_fraction:
                self.is_ordinal = (
                    self.is_ordinal_word(word)
                )
            else:
                self.is_ordinal = False

            # Leading zeros after decimal point
            if (
                decimal_point
                and number == 0
                and buffer in (None, 0)
            ):
                leading_zeros += 1

            # Standalone fraction
            if is_fraction and buffer is None:
                value = 1 / number

                if integer_part is not None:
                    value += integer_part

                value += total

                self.value = apply_sign(value)
                self.is_ordinal = False

                return " ".join(parsed_words)

            # First number
            if buffer is None:
                buffer = number
                parts = [number]
                continue

            # Fraction
            if is_fraction and numerator is None:

                if number >= 10 or len(parts) == 1:
                    fraction = buffer / number

                else:
                    denominator = number
                    index = len(parts)

                    for i in range(
                        len(parts) - 1,
                        0,
                        -1,
                    ):
                        part = parts[i]

                        if not self.is_free_digit(
                            denominator,
                            part,
                        ):
                            break

                        denominator += part
                        index = i

                    fraction = (
                        sum(parts[:index])
                        / denominator
                    )

                if integer_part is not None:
                    fraction += integer_part

                fraction += total

                self.value = apply_sign(fraction)
                self.is_ordinal = False

                return " ".join(parsed_words)

            # Normal number
            #
            # twenty five:
            # 20 -> 5 = 25
            #
            # five twenty:
            # 5 -> 20 = two different numbers
            if (
                number < buffer
                and self.is_free_digit(
                    buffer,
                    number,
                )
            ):
                buffer += number
                parts.append(number)

            else:
                if numerator is None:
                    numerator = buffer

                    # Current word belongs to
                    # the next number
                    first_number_words = (
                        parsed_words[:-1].copy()
                    )

                buffer = number
                parts = [number]

            # Compound denominator:
            # тринадцать тридцать пятых
            if is_fraction:
                value = numerator / buffer

                if integer_part is not None:
                    value += integer_part

                value += total

                self.value = apply_sign(value)
                self.is_ordinal = False

                return " ".join(parsed_words)

        if (
            buffer is None
            and integer_part is None
            and total == 0
        ):
            raise ParseError(
                f"Number not found: {from_string!r}"
            )

        # Decimal
        if (
            integer_part is not None
            and decimal_point
        ):
            self.value = apply_sign(
                decimal_value()
            )

            self.is_ordinal = False

            return " ".join(parsed_words)

        # Scale result
        if buffer is None:
            self.value = apply_sign(total)

            return " ".join(parsed_words)

        # Normal number
        current = (
            buffer
            if numerator is None
            else numerator
        )

        self.value = apply_sign(
            total + current
        )

        if (
            numerator is not None
            and first_number_words
        ):
            return " ".join(
                first_number_words
            )

        return " ".join(parsed_words)


pattern_parser.register_parameter_type(
    NLNumberRU
)