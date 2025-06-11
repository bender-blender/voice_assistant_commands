from typing_extensions import NamedTuple
import requests
from geopy.geocoders import Nominatim


class Coordinates(NamedTuple):
    latitude: float
    longitude: float

class LocationProvider:

    def get_coordinates(self, location_name: str | None = None) -> Coordinates:

        if location_name:
            return self._coordinates_from_name(location_name)

        if self.home:
            return self.home

        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        place = data.get("city")

        if not place:
            raise ValueError("Can't determine the city by IP")

        self.home = home = self._coordinates_from_name(place)

        return home

    def _coordinates_from_name(self, location_str: str) -> Coordinates:
        location = Nominatim(user_agent="geo_app").geocode(location_str)
        return Coordinates(location.latitude, location.longitude)
