from dataclasses import dataclass
from datetime import datetime

from dateparser import parse
from icalendar import Event


@dataclass
class ReminderModel:
    event_summary: str | None = None
    event_time: str | None = None
    event_date: str | None = None
    event_location: str | None = None

    def make_event(self) -> Event:
        event = Event()

        current_year = datetime.now().year
        dt_start = parse(f"{self.event_time} {self.event_date} {current_year}", languages=["ru"])

        if dt_start and dt_start < datetime.now():
            dt_start = parse(
                f"{self.event_time} {self.event_date} {current_year + 1}",
                languages=["ru"],
            )

        if not dt_start:
            raise ValueError("Неверная дата/время")

        event.add("summary", self.event_summary)
        event.add("dtstart", dt_start)

        if self.event_location:
            event.add("location", self.event_location)

        return event
