from ..model.model_note import ModelReminder
from ..custom_types import Day, Time, Year
from icalendar import Event, Calendar
from stark.core.types import String
from datetime import datetime
from dateparser import parse
from stark import Response
import anyio


class RemindersProvider:

    def __init__(self):
        self.calendar = Calendar()
        self.events: list[ModelReminder] = []

        # provider should be stateless, and definitely must not store current context; use commands' context instead
        # self.current_reminder = None
        # self.summary: str = None
        # self.time: str = None
        # self.date: str = None
        # self.year: str = None
        # self.location: str = None

    def create_reminder(self):
        if self.current_reminder != None:
            return Response(voice="Заметка уже создана")

        self.current_reminder = Event()

    def add_summary(self, content: String):
        if self.current_reminder is None:
            return Response(voice="Создайте заметку")

        if self.summary != None:
            return Response(voice="Описание уже добавлено")

        self.summary = content.value


    def add_time(self, content: Time):

        if self.current_reminder is None:
            return Response(voice="Создайте заметку")

        if self.time is not None:
            return Response(voice="Время уже добавлено")

        self.time = content.hour


    def add_date(self, content: Day):

        if self.current_reminder is None:
            return Response(voice="Создайте заметку")

        if self.date is not None:
            return Response(voice="Дата уже добавлена")

        self.date = content.day


    def add_year(self, content: Year):

        if self.current_reminder == None:
            return Response(voice="Создайте заметку")

        if self.year is not None:
            return Response(voice="Год уже добавлен")

        self.year = content.year


    def add_location(self, content: String):
        if self.current_reminder is None:
            return Response(voice="Создайте заметку")

        if self.location is not None:
            return Response(voice="Место уже добавлено")

        self.location = content.value



    def save(self, file_path="reminders.ics"):

        if not self.year:
            self.year = str(datetime.now().year)

        reminder = ModelReminder(
            event_summary=self.summary,
            event_time=self.time,
            event_date=self.date,
            event_year=self.year,
            event_location=self.location
        )


        try:
            event = reminder.to_event()
            self.calendar.add_component(event)

        except ValueError:
            self.current_reminder = None
            self.summary = self.time = self.date = self.year = self.location = None
            #return Response(voice=f"Ошибка при создании события")

        self.events.append(reminder)

        with open(file_path, 'wb') as f:
            f.write(self.calendar.to_ical())

        self.current_reminder = None
        self.summary = self.time = self.date = self.year = self.location = None


    async def reminder_loop(self):
        while True:
            now = datetime.now()

            # Копируем список событий, чтобы можно было безопасно изменять оригинал
            for reminder in self.events[:]:

                full_time_str = f"{reminder.event_time} {reminder.event_date} {reminder.event_year}"
                event_time = parse(full_time_str)

                if not event_time:
                    # Не удалось распарсить дату — пропускаем
                    continue

                if event_time <= now:

                    self.events.remove(reminder)

                    # Удаляем событие из календаря
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
