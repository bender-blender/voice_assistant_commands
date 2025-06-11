from dataclasses import dataclass
from icalendar import Calendar,Event
from dateparser import parse


@dataclass
class ReminderModel:

    event_summary: str | None = None
    event_time: str | None = None
    event_date: str | None = None
    event_year: str | None = None
    event_location: str | None = None

    def make_event(self) -> Event:
        event = Event()

        full_datetime_str = f"{self.event_time} {self.event_date} {self.event_year}"
        dt_start = parse(full_datetime_str) # parameter model must parse everything to datetime

        if not dt_start:
            raise ValueError("Неверная дата/время")

        event.add('summary', self.event_summary)
        event.add('dtstart', dt_start)

        if self.event_location:
            event.add('location', self.event_location)

        return event
