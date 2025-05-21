from dataclasses import dataclass
from geopy.geocoders import Nominatim

@dataclass
class CityInfo:
    location: str

    def get_coordinates(self):
        geolocator = Nominatim(user_agent="geo_app")
        location = geolocator.geocode(self.location)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None

