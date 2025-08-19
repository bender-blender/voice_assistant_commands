import unittest
from voice_commands.apps.clock.alarm.provider.alarm_provider import ProviderAlarm
from stark.core.types import String
from voice_commands.parameters import Time

class TestAlarmProvider(unittest.TestCase):

    def setUp(self) -> None:
        self.alarm = ProviderAlarm()
    
    def test_add_name(self):

        list_name = ["Подъем", "Работа", "Ужин"] 
        for name in list_name:
            self.alarm.add_name(String(name))
            self.assertEqual(self.alarm.name, name)
    
    def test_add_target_time(self):
        list_time = [(6, 30), (8, 0), (19, 15)]
        for time in list_time:
            self.alarm.add_target_time(Time(time))
            self.assertEqual(self.alarm.target_time, time)
    
    def test_add_day(self):
        list_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Каждый день"]
        for day in list_days:
            self.alarm.add_day(String(day))
            self.assertEqual(self.alarm.day.lower(), day.lower())

    def test_start_alarm(self):
        list_name = ["Подъем", "Работа", "Ужин"] 
        list_time = [(6, 30), (8, 0), (19, 15)]
        list_days = ["Понедельник", "Вторник", "Среда"]
        
        for name, time, day in zip(list_name, list_time, list_days):
            self.alarm.add_name(String(name))
            self.alarm.add_target_time(Time(time))
            self.alarm.add_day(String(day.lower()))
            self.alarm.start_alarm()
            self.assertIn(name, self.alarm.model.list_jobs)
            self.assertEqual(self.alarm.model.list_jobs[name][0], f"{time[0]:02d}:{time[1]:02d}")
            self.assertEqual(self.alarm.model.list_jobs[name][1], day.lower())


if __name__ == "__main__":
    unittest.main()
