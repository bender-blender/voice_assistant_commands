import requests
from geopy.geocoders import Nominatim
from typing_extensions import NamedTuple


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


class LocationProvider:
    def __init__(self):
        self.home: Coordinates | None = None

    async def get_coordinates(self, location_name: str | None = None) -> Coordinates:
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

    def _coordinates_from_name(self, location_str: str) -> Coordinates | None:
        geolocator = Nominatim(user_agent="geo_app", timeout=5)
        location = geolocator.geocode(location_str)
        if not location:
            return None  # Нельзя обращаться к location.raw, если location — None

        raw = location.raw
        loc_type = raw.get("type", "")
        if loc_type in ("city", "administrative", "country", "residential"):
            return Coordinates(int(location.latitude), int(location.longitude))

        return None
