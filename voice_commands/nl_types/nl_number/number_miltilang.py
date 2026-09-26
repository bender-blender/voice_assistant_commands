from number_parser import parse_number, parse_ordinal

from stark.core.parsing import Pattern, ParseError
from stark.core.types import Object
from stark.general.classproperty import classproperty

from voice_commands.nl_types.parsing_context import pattern_parser


class NLMultiNumber(Object):
    value: float
    is_ordinal: bool

    locale = "en_US"

    fractions = {
        "half": 2,
        "halves": 2,
        "quarter": 4,
        "quarters": 4,
        "third": 3,
        "thirds": 3,
    }

    @classproperty
    def pattern(cls):
        return Pattern("**")

    def get_number(self, words):
        for start in range(len(words)):
            for end in range(len(words), start, -1):
                part = words[start:end]
                text = " ".join(part)

                last = part[-1]

                is_ordinal = (
                    parse_number(last) is None
                    and parse_ordinal(last) is not None
                )

                value = (
                    parse_ordinal(text)
                    if is_ordinal
                    else parse_number(text)
                )

                if value is not None:
                    return value, is_ordinal, part, start

        return None

    async def did_parse(self, from_string):
        words = (
            str(from_string)
            .lower()
            .replace("-", " ")
            .split()
        )

        # Decimal numbers
        if "point" in words:
            i = words.index("point")

            left = self.get_number(words[:i])

            if left:
                value, _, left_words, start = left

                right = []
                sub = []

                for word in words[i + 1:]:
                    number = parse_number(word)

                    if number is None:
                        break

                    right.append(str(int(number)))
                    sub.append(word)

                if right:
                    negative = (
                        start > 0
                        and words[start - 1] == "minus"
                    )

                    self.value = float(
                        f"{value}.{''.join(right)}"
                    )

                    if negative:
                        self.value *= -1

                    self.is_ordinal = False

                    result = (
                        left_words
                        + ["point"]
                        + sub
                    )

                    if negative:
                        result.insert(0, "minus")

                    return " ".join(result)

        # Fractions
        for i, word in enumerate(words):
            if word not in self.fractions:
                continue

            denominator = self.fractions[word]

            # half / quarter
            if (
                i == 0
                and word in ("half", "quarter")
            ):
                self.value = 1 / denominator
                self.is_ordinal = False

                return word

            # two and a half
            if "and" in words[:i]:
                j = max(
                    index
                    for index, value in enumerate(words[:i])
                    if value == "and"
                )

                whole = self.get_number(
                    words[:j]
                )

                if whole:
                    numerator = self.get_number(
                        words[j + 1:i]
                    )

                    fraction = (
                        numerator[0]
                        if numerator
                        else 1
                    )

                    self.value = (
                        whole[0]
                        + fraction / denominator
                    )

                    self.is_ordinal = False

                    return " ".join(
                        words[whole[3]:i + 1]
                    )

            # a half / a quarter
            if (
                i
                and words[i - 1] == "a"
            ):
                self.value = 1 / denominator
                self.is_ordinal = False

                return f"a {word}"

            numerator = self.get_number(
                words[:i]
            )

            if numerator:
                value, _, part, start = numerator

                # twenty third -> ordinal
                # one third -> fraction
                if (
                    not word.endswith("s")
                    and word not in ("half", "quarter")
                    and value != 1
                ):
                    continue

                self.value = (
                    value / denominator
                )

                self.is_ordinal = False

                if (
                    start > 0
                    and words[start - 1] == "minus"
                ):
                    self.value *= -1
                    part = ["minus"] + part

                return " ".join(
                    part + [word]
                )

        # Normal / ordinal numbers
        result = self.get_number(words)

        if result:
            value, ordinal, part, start = result

            negative = (
                start > 0
                and words[start - 1] == "minus"
            )

            self.value = (
                -value
                if negative
                else value
            )

            self.is_ordinal = ordinal

            if negative:
                part = ["minus"] + part

            return " ".join(part)

        raise ParseError("number not found")


pattern_parser.register_parameter_type(
    NLMultiNumber
)