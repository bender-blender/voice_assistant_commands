from ..model.alarm_model import AlarmModel
from stark.core.types import String
from voice_commands.parameters import Time
import schedule


class ProviderAlarm:

    def __init__(self) -> None:
        self.model = AlarmModel()

        self.name: str
        self.day: str

        self.target_time: tuple

    def add_name(self, name: String) -> None:
        self.name = name.value

    def add_target_time(self, target_time: Time) -> None:
        self.target_time = target_time.value

    def add_day(self, day: String) -> None:
        self.day = day.value

    def start_alarm(self) -> None:
        validation_date = f"{self.target_time[0]}:{self.target_time[1]}"
        if len(validation_date.split(':')[0]) == 1:
            target_time = f"0{self.target_time}"

        def call_alarm():
            print(f"Будильник {self.name} сработал")
            return call_alarm

        day = self.day.lower()
        if "понедельник" in day:
            create_task = schedule.every().monday.at(target_time).do(call_alarm)
        elif "вторник" in day:
            create_task = schedule.every().tuesday.at(target_time).do(call_alarm)
        elif "сред" in day:
            create_task = schedule.every().wednesday.at(target_time).do(call_alarm)
        elif "четверг" in day:
            create_task = schedule.every().thursday.at(target_time).do(call_alarm)
        elif "пятниц" in day:
            create_task = schedule.every().friday.at(target_time).do(call_alarm)
        elif "суббот" in day:
            create_task = schedule.every().saturday.at(target_time).do(call_alarm)
        elif "воскресенье" in day:
            create_task = schedule.every().sunday.at(target_time).do(call_alarm)
        elif "каждый день" in day:
            create_task = schedule.every().day.at(target_time).do(call_alarm)

        self.model.list_jobs[self.name] = (target_time, day, create_task)
        self.name = ""
        self.target_time = ()
        self.day = ""

    def cancel_alarm(self, name:String) -> None:
        alarm = name.value
        self.model.cancel_alarm(alarm)

    def get_alarm(self) -> None:
        self.model.see_alarm()
