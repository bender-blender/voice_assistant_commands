from geopy.distance import geodesic, Distance
from geopy.geocoders import Nominatim
from geopy.point import Point
from asyncer import asyncify
import asyncio
import httpx


from typing_extensions import NamedTuple,TypedDict,Dict
import math


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


class PlaceInfo(TypedDict):
    distance_km: Distance
    coordinates: Coordinates
    opening_hours: str




class LocationProvider:
    
    def __init__(self):
        self.cache_place: dict[str, dict[str,PlaceInfo] | dict[str,Coordinates]] = {}  # point storage
        self.home: Coordinates | None = None
        self.name_point = None
        self.geolocator = Nominatim(user_agent="geo_app", timeout=5)
        

    @asyncify
    def _geocode_sync(self,location_str: str) -> Coordinates | None:
        return self.coordinates_from_name(location_str)
    

    async def get_coordinates(self, location_name: str | None = None) -> Coordinates | None:
        """
        Get the coordinates of a home point
        :param location_name: name 
        :type location_name: str | None if the parameter is missing, the provider's location
        :return: Named tuple or None in the absence of coordinates
        :rtype: Coordinates | None
        """
        if location_name:
            await asyncio.sleep(0.1)
            self.home = await self._geocode_sync(location_name)
            self.name_point = location_name
            return self.home

        if self.home:
            return self.home
        
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get("http://ip-api.com/json/")
            response.raise_for_status()
            data = response.json()
        
        place = data.get("city")

        if not place:
            raise ValueError("Can't determine the city by IP")

        self.home = await self._geocode_sync(place)
        self.name_point = place

        return self.home
        

    def coordinates_from_name(self, location_str: str, timeout: int = 10) -> Coordinates | None:
        """
        Get coordinates of ANY location
        
        :param location_str: name
        :type location_str: str
        :param timeout: for API
        :type timeout: int
        :return: Named tuple or None in the absence of coordinates
        :rtype: Coordinates | None
        """
        
        location = self.geolocator.geocode(location_str,addressdetails=True)
        if not location:
            return None

        return Coordinates(location.latitude, location.longitude)
    

    


    async def _get_list_of_tags(self, place: str, radius_in_kilometers: float | None = None) -> Dict[str,PlaceInfo] | Dict[str, Coordinates]:
        """
        Docstring для _get_list_of_tags
        
        :param place: name
        :type place: str
        :param radius_in_kilometers: search for objects within a radius (in kilometers)
        :type radius_in_kilometers: float
        :return: Dictionary of the format 'name: {full address:{distance,coordinates,opening hours}(PlaceInfo)'
        :rtype: Dict[str, PlaceInfo] | Dict[str, Coordinates]
        """
        if not isinstance(self.home, Coordinates):
            raise ValueError("Home location is not set")
        

        if not isinstance(self.name_point,str):
            raise ValueError("Home location is not set")


        if place in self.cache_place:
            return self.cache_place[place]
        
        
        if radius_in_kilometers is None:
            coords = self.coordinates_from_name(place)
            if coords is None:
                return {}
        
            place_info: PlaceInfo = {
                "distance_km": Distance(0),
                "coordinates": coords,
                "opening_hours": "не указано"
            }

            return {place: place_info}
        
        home_lat = self.home.latitude
        home_lon = self.home.longitude
        lat_delta = radius_in_kilometers / 111.0
        lon_delta = radius_in_kilometers / (
            111.0 * math.cos(math.radians(home_lat))
        )

        viewbox = (
            Point(home_lat - lat_delta, home_lon - lon_delta),
            Point(home_lat + lat_delta, home_lon + lon_delta)
        )

        
        result = self.geolocator.geocode(
            query=f"{place}",
            limit=50,
            exactly_one=False,
            addressdetails=True,
            extratags=True,
            viewbox=viewbox,
            bounded=True
        )
        if not result:
            return {}

        

        matches_found: dict[str, dict[str, PlaceInfo]] = {}
        matches_found[place] = {}
        for loc in result:
            address = loc.address
            loc_lat = float(loc.latitude)
            loc_lon = float(loc.longitude)

            distance = geodesic(
                (loc_lat, loc_lon),
                (home_lat, home_lon)
            ).km

            extratags = loc.raw.get("extratags") or {}
            hours = extratags.get("opening_hours", "не указано")
            
            
            place_info: PlaceInfo = {
               "distance_km": distance,
               "coordinates": Coordinates(loc_lat, loc_lon),
               "opening_hours": hours
            }
            
            matches_found[place][address] = place_info
        
        
        self.cache_place[place] = dict(sorted(matches_found[place].items(),
                                              key=lambda item: item[1]["distance_km"]))
        return self.cache_place[place]