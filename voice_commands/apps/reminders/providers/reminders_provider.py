from datetime import datetime

import anyio
from dateparser import parse
from icalendar import Calendar, Event
from stark import Response
from stark.core.types import String

from ..model.reminder import ReminderModel
from voice_commands.parameters import Day,Time


class RemindersProvider:
    def __init__(self) -> None:
        self.calendar = Calendar()
        self.events: list[ReminderModel] = []

    def create_reminder(self):
        self.current_reminder = Event()

    def add_summary(self, content: String):
        self.summary = content.value

    def add_time(self, content: Time):
        self.time = f"{content.value[0]}:{content.value[1]}"

    def add_date(self, content: Day):
        self.date = content.value

    def add_location(self, content: String):
        self.location = content.value

    def save(self, file_path="reminders.ics"):
        reminder = ReminderModel(
            event_summary=self.summary,
            event_time=self.time,
            event_date=self.date,
            event_location=self.location,
        )

        try:
            event = reminder.make_event()
            self.calendar.add_component(event)

        except ValueError:
            self.current_reminder = None
            self.summary = self.time = self.date = self.location = None

        self.events.append(reminder)

        with open(file_path, "wb") as f:
            f.write(self.calendar.to_ical())

        self.current_reminder = None
        self.summary = self.time = self.date = self.location = None

    async def reminder_loop(self):
        while True:
            now = datetime.now().replace(tzinfo=None)

            for reminder in self.events[:]:
                full_time_str = f"{reminder.event_time} {reminder.event_date} {now.year}"
                event_time = parse(
                    full_time_str,
                    languages=["ru"],
                    settings={"DATE_ORDER": "DMY"}
                )

                if not event_time:
                    continue

                if event_time.tzinfo:
                    event_time = event_time.replace(tzinfo=None)

                # переносим на следующий год только если событие уже прошло в этом году
                if event_time.date() < now.date():
                    event_time = parse(
                        f"{reminder.event_time} {reminder.event_date} {now.year + 1}",
                        languages=["ru"],
                        settings={"DATE_ORDER": "DMY"}
                    )
                    if event_time and event_time.tzinfo:
                        event_time = event_time.replace(tzinfo=None)

                # проверяем окно в 1 сек
                if event_time and abs((event_time - now).total_seconds()) <= 1:
                    

                    self.events.remove(reminder)

                    for component in list(self.calendar.subcomponents):
                        if (
                            component.name == "VEVENT"
                            and str(component.get("summary")) == str(reminder.event_summary)
                            and str(component.get("location")) == str(reminder.event_location)
                        ):
                            self.calendar.subcomponents.remove(component)
                            break

                    with open("reminders.ics", "wb") as f:
                        f.write(self.calendar.to_ical())

                    yield Response(voice=f"Событие «{reminder.event_summary}» наступило")

            await anyio.sleep(1)
