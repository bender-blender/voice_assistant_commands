import unittest

from voice_commands.apps.reminders.providers.reminders_provider import RemindersProvider
from icalendar import Event
from stark.core.types import String
from voice_commands.apps.reminders.parameters import Day,Time


class TestReminder(unittest.TestCase):

    def setUp(self) -> None:
        self.reminder = RemindersProvider()

    def test_create_reminder(self) -> None:
        self.reminder.create_reminder()
        self.assertEqual(self.reminder.current_reminder,Event())
    
    def test_add_summary(self) -> None:
        self.reminder.add_summary(String("Приглашение на свадьбу"))
        self.assertEqual(self.reminder.summary, "Приглашение на свадьбу")
    
    def test_add_location(self) -> None:
        self.reminder.add_location(String("Город Одесса"))
        self.assertEqual(self.reminder.location,"Город Одесса")

        


class AsyncTest(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self) -> None:
        self.reminder = RemindersProvider()
    
    async def test_add_time(self) -> None:
        time = Time(None)
        await time.did_parse("пятнадцать тридцать")
        self.reminder.add_time(time)
        
        self.assertEqual(self.reminder.time,"15:30")

    async def test_add_date(self) -> None:
        day = Day(None)
        await day.did_parse("второе сентября")
        self.reminder.add_date(day)
        self.assertEqual(self.reminder.date,"2 сентября")

    async def test_save(self) -> None:
        self.reminder.create_reminder()
        self.reminder.add_summary(String("Приглашение на свадьбу"))
        self.reminder.add_location(String("Город Одесса"))
        time = Time(None)
        await time.did_parse("пятнадцать тридцать")
        self.reminder.add_time(time)
        day = Day(None)
        await day.did_parse("второе сентября")
        self.reminder.add_date(day)

        self.reminder.save()
        self.assertEqual(all(self.reminder.events),True)


if __name__ == "__main__":
    unittest.main()
