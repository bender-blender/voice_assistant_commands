from datetime import datetime
from icalendar import Event, Calendar
from stark import Response
from stark.core.types import String, MyTime, MyHours, MyYear
import dateparser
import anyio


class Note:
    """
    Класс управления заметками. Позволяет создавать события, добавлять описание, дату и локацию.
    Автоматически сохраняет в .ics и напоминает за 15 минут через S.T.A.R.K.
    """

    def __init__(self):
        self.calendar = Calendar()
        self.current_note = None
        self.is_summary = False
        self.is_start_date = False
        self.is_time = False
        self.is_year = False
        self.is_location = False
        self.event_date = None
        self.event_time = None
        self.event_year = None
        self.event_location = None
        self.event_summary = None
        self.events = []  # Список событий

    def create_a_note(self):
        """Создать заметку"""
        if self.current_note is not None:
            return Response(voice="Заметка уже создана")

        self.current_note = Event()
        return Response(voice="Заметка создана")

    def add_summary(self, content: String):
        """Добавить описание"""
        if self.current_note is None:
            return Response(voice="Для начала, создайте заметку")

        if self.is_summary:
            return Response(voice="Описание уже добавлено")

        self.event_summary = content.value
        self.is_summary = True
        return Response(voice="Описание добавлено")

    def add_time(self, day: MyTime):
        """Добавить дату"""
        if self.current_note is None:
            return Response(voice="Для начала, создайте заметку")

        if self.is_time:
            return Response(voice="Дата уже добавлена")

        self.event_date = day.mytime_day  # Сохраняем дату
        self.is_time = True
        return Response(voice="Дата добавлена")

    def start_date(self, hour: MyHours):
        """Добавить время"""
        if self.current_note is None:
            return Response(voice="Для начала, создайте заметку")

        if self.is_start_date:
            return Response(voice="Время уже добавлено")

        if not hour or not hour.myhours_hour:
            return Response(voice="Время не распознано, пожалуйста повторите")

        self.event_time = hour.myhours_hour.strip()
        self.is_start_date = True
        return Response(voice=f"Время {self.event_time} добавлено")

    def add_location(self, content: String):
        """Добавить место события"""
        if self.current_note is None:
            return Response(voice="Для начала, создайте заметку")

        if self.is_location:
            return Response(voice="Локация уже добавлена")

        self.event_location = content.value  # Сохраняем место
        self.is_location = True
        return Response(voice="Локация добавлена")

    def add_year(self, year: MyYear):
        """Добавить год
        """
        if self.current_note is None:
            return Response(voice="Для начала, создайте заметку")

        if self.is_year:
            return Response(voice="Год уже добавлен")

        self.event_year = year.myyear_year
        self.is_year = True
        return Response(voice="Год добавлен")

    def save_event(self):
        """Сохранить событие и добавить в список для напоминаний"""
        if self.current_note is None:
            return Response(voice="Нет созданной заметки для сохранения")

        if not (self.event_date and self.event_time and self.event_summary):
            return Response(voice="Заполните описание, дату и время перед сохранением")

        if self.event_year is None:
            self.event_year = datetime.now().year

        try:
            event_start = dateparser.parse(
                f"{self.event_date} {self.event_year} {self.event_time}")
            print(event_start)
            self.current_note.add("summary", self.event_summary)
            self.current_note.add("dtstart", event_start)
            if self.event_location:
                self.current_note.add("location", self.event_location)

            self.calendar.add_component(self.current_note)

            self.events.append({
                "summary": self.event_summary,
                "time": event_start
            })

            with open("events.ics", "wb") as f:
                f.write(self.calendar.to_ical())


            # Сброс
            self.current_note = None
            self.is_summary = False
            self.is_start_date = False
            self.is_time = False
            self.is_year = False
            self.is_location = False
            self.event_date = None
            self.event_time = None
            self.event_year = None
            self.event_location = None
            self.event_summary = None

            return Response(voice="Событие успешно сохранено")
        except Exception as e:
            
            self.current_note = None
            self.is_summary = False
            self.is_start_date = False
            self.is_time = False
            self.is_year = False
            self.is_location = False
            self.event_date = None
            self.event_time = None
            self.event_year = None
            self.event_location = None
            self.event_summary = None

            return Response(voice=f"Ошибка при сохранении события: {str(e)}", text=f"Ошибка при сохранении события: {str(e)}")


    async def reminder_loop(self):
        while True:
            now = datetime.now()
            for event in self.events[:]:
                event_time = event.get("time")

                if isinstance(event_time, str):
                    try:
                        event_time = dateparser.parse(event_time)
                    except Exception:
                        continue

                if event_time <= now:
                    self.events.remove(event)

                # Удаляем из календаря
                    for component in list(self.calendar.subcomponents):
                        if component.name == "VEVENT" and component.get("summary") == event["summary"]:
                            self.calendar.subcomponents.remove(component)
                            break

                # Обновляем файл
                    with open("events.ics", "wb") as f:
                        f.write(self.calendar.to_ical())

                # Генерируем ответ
                    yield Response(voice=f"Событие {event['summary']} наступило")

            await anyio.sleep(1)



