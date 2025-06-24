from ..model.reminder import ReminderModel
from ..parameters import Day,Time
from icalendar import Event, Calendar
from stark.core.types import String
from datetime import datetime
from dateparser import parse
from stark import Response
import anyio


class RemindersProvider:

    def __init__(self):
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
            event_location=self.location
        )


        try:
            event = reminder.make_event()
            self.calendar.add_component(event)

        except ValueError:
            self.current_reminder = None
            self.summary = self.time = self.date = self.location = None


        self.events.append(reminder)

        with open(file_path, 'wb') as f:
            f.write(self.calendar.to_ical())

        self.current_reminder = None
        self.summary = self.time = self.date = self.location = None


    async def reminder_loop(self):
        while True:
            now = datetime.now()

            for reminder in self.events[:]:
                current_year = now.year
                full_time_str = f"{reminder.event_time} {reminder.event_date} {current_year}"

                event_time = parse(full_time_str, languages=['ru'])

                # Если дата распарсилась, но в прошлом — сдвигаем на следующий год
                if event_time and event_time < now:
                    event_time = parse(f"{reminder.event_time} {reminder.event_date} {current_year + 1}", languages=['ru'])

                if not event_time:
                    # Не удалось распарсить дату — пропускаем
                    continue

                if event_time <= now:
                    self.events.remove(reminder)

                    for component in list(self.calendar.subcomponents):
                        if (component.name == "VEVENT" and
                            component.get("summary") == reminder.event_summary and
                            component.get("location") == reminder.event_location):
                            self.calendar.subcomponents.remove(component)
                            break

                    with open("reminders.ics", "wb") as f:
                        f.write(self.calendar.to_ical())

                    yield Response(voice=f"Событие «{reminder.event_summary}» наступило")

            await anyio.sleep(1)
