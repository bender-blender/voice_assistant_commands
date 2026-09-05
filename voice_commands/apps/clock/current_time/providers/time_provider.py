from datetime import datetime

# from stark import Response # not allowed in providers
import pytz
from timezonefinder import TimezoneFinder

from voice_commands.providers.location_provider import Coordinates


class TimeProvider:
    def get_time(self, location: Coordinates | None = None) -> datetime:
        if not location:
            return datetime.now()

        timezone_str = TimezoneFinder().timezone_at(lat=location.latitude, lng=location.longitude)

        if not timezone_str:
            raise ValueError("Could not determine timezone for the given location.")

        local_time = datetime.now(pytz.timezone(timezone_str))

        return local_time
