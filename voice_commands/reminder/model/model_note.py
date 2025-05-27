from dataclasses import dataclass
from icalendar import Calendar,Event
from dateparser import parse


@dataclass
class ModelReminder:
    event_summary : str = None
    event_time : str = None
    event_date : str = None
    event_year : str = None
    event_location : str = None

    def to_event(self) -> Event:
        event = Event()
        full_datetime_str = f"{self.event_time} {self.event_date} {self.event_year}"
        dt_start = parse(full_datetime_str)
        if not dt_start:
            raise ValueError("Неверная дата/время")

        event.add('summary', self.event_summary)
        event.add('dtstart', dt_start)
        if self.event_location:
            event.add('location', self.event_location)
        return event