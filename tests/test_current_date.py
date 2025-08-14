import datetime
import time
import unittest

from voice_commands.apps.clock.current_time.providers.time_provider import TimeProvider
from voice_commands.apps.clock.stopwatch.providers.stopwatch_provider import (
    StopwatchProvider,
)
from voice_commands.apps.clock.timer.parameters.interval import Interval
from voice_commands.apps.clock.timer.providers.provider_timer import TimerProvider


class TestClock(unittest.TestCase):
    def setUp(self) -> None:
        self.time = TimeProvider()
        self.stopwatch = StopwatchProvider()

    def test_time(self) -> None:
        time = self.time.get_time().strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(time, now)

    def test_stopwatch(self) -> None:
        self.stopwatch.start()
        time.sleep(3)
        stop = round(self.stopwatch.elapsed())
        self.assertEqual(stop, 3)


class TestTimer(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.timer = TimerProvider()

    async def test_timer(self) -> None:
        interval = Interval(None)
        await interval.did_parse("пять минут")
        result = self.timer.set_a_timer(interval)
        self.assertEqual(result, 300)


if __name__ == "__main__":
    unittest.main()
