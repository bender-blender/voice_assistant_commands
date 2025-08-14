# TODO: Implement custom class
from datetime import time

from stark.core.patterns import Pattern
from stark.core.types import Object, ParseError, String
from stark.general.classproperty import classproperty

from ....formatters import TimeFormatter
from .data_dictionary import GeneralDictionary


class Time(Object):
    hour: String
    numbers = GeneralDictionary().words_to_numbers

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$hour:String")

    async def did_parse(self, from_string) -> str:
        words = [w for w in from_string.lower().split() if not w.startswith(("час", "минут")) and w != "ровно"]

        if not words:
            raise ParseError("Не удалось распознать время. Попробуйте снова.")

        nums = [self.numbers.get(w, -1) for w in words]

        if -1 in nums:
            raise ParseError(f"Неизвестные слова во времени: {' '.join(words)}")

        if len(nums) >= 2 and nums[0] in [20, 30, 40, 50] and nums[1] < 10:
            hour = nums[0] + nums[1]
            minute = sum(nums[2:])
        else:
            hour = nums[0]
            minute = sum(nums[1:])

        if not (0 <= hour <= 23):
            raise ParseError(f"Некорректный час: {hour}")
        if not (0 <= minute <= 59):
            raise ParseError(f"Некорректные минуты: {minute}")

        parsed_time = time(hour=hour, minute=minute)

        self.hour = TimeFormatter(target_datetime=parsed_time).get_formatted_time()  # type: ignore
        self.value = self.hour

        return from_string


Pattern.add_parameter_type(Time)
