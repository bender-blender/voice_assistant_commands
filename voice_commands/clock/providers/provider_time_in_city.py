from ...models.model_city import CityInfo
from ...models.model_time import TimeModel
from timezonefinder import TimezoneFinder
from stark.core.types import String
from datetime import datetime
from stark import Response
import pytz


class TimeCityProvider:
    
    def __init__(self, location: String):
        self.location = location

    def get_time_by_coordinates(self):
        tf = TimezoneFinder()
        coordinates = CityInfo(self.location).get_coordinates()
        
        if (
        not coordinates or
        not isinstance(coordinates, tuple) or
        len(coordinates) != 2 or
        coordinates[0] is None or
        coordinates[1] is None
        ):
            return Response(voice="Не удалось определить координаты")
        
        timezone_str = tf.timezone_at(lat=coordinates[0], lng=coordinates[1])
        if timezone_str:
            tz = pytz.timezone(timezone_str)
            local_time = datetime.now(tz)
            return TimeModel(local_time)
        else:
            return Response(voice="Не удалось определить часовой пояс")