from voice_commands.apps.clock.alarm.parameters.time_alarm import WeekDay
from voice_commands.parameters import Time
from ..model.alarm_model import AlarmModel
from stark.core.types import String
from typing import Tuple, List, Dict
import schedule


class ProviderAlarm:

    def __init__(self) -> None:
        self.model = AlarmModel()

        self.name: str
        self.day: List[Tuple[str,schedule.Job]] | None
        self.target_time: str

    def add_name(self, name: String) -> None:
        self.name = name.value

    def add_target_time(self, target_time: Time) -> None:
        number_hours, number_minutes = target_time.value
        self.target_time = f"{number_hours:02d}:{number_minutes:02d}"


    def add_day(self, day: WeekDay) -> None:
        self.day = day.value

    def start_alarm(self) -> None:
        def call_alarm():
            print(f"Будильник {self.name} сработал")
            return call_alarm
        
        if self.day is not None:
            for day in self.day:
                task = day[1].at(self.target_time).do(call_alarm)
                if self.name not in self.model.list_jobs:
                    self.model.list_jobs[self.name] = [(self.target_time, day[0], task)]
                else:
                    self.model.list_jobs[self.name].append((self.target_time, day[0], task))
        self.name = ""
        self.target_time = ""
        self.day = None

    def cancel_alarm(self, name:String) -> None:
        alarm = name.value
        self.model.cancel_alarm(alarm)

    def get_alarm(self) -> Dict[str, List[tuple[str, str, schedule.Job]]]:
        alarms = self.model.see_alarm()
        return alarms
