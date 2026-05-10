from geopy.distance import geodesic, Distance
from geopy.geocoders import Nominatim
from async_lru import alru_cache
from geopy.point import Point
from asyncer import asyncify
import asyncio
import httpx

from typing_extensions import NamedTuple

import math
from dataclasses import dataclass

class Coordinates(NamedTuple):
    latitude: float
    longitude: float


@dataclass
class PlaceInfo:
    distance_km: Distance
    coordinates: Coordinates
    opening_hours: str




class LocationProvider:
    
    home_coordinates = None

    geolocator = Nominatim(user_agent="geo_app", timeout=5)
    

    async def fetch_home_coordinates_if_needed(self, location_name: str | None = None):
        if not self.home_coordinates:
            await self.fetch_home_coordinates(location_name)
        
    
    async def fetch_home_coordinates(self, location_name: str | None = None):
        """
        Update the home point.
        :param location_name: name 
        :type location_name: str | None if the parameter is missing, the provider's location
        :return: Named tuple or None in the absence of coordinates
        :rtype: Coordinates | None
        """
        
        # try to get coordinates by location name if it is provided
        
        if location_name:
            await asyncio.sleep(0.1)
            self.home_coordinates = await asyncify(self.coordinates_from_name)(location_name)
            self.name_point = location_name
            return self.home_coordinates

        # Location name is not provided, try to determine it by IP
        
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get("http://ip-api.com/json/")
            response.raise_for_status()
            data = response.json()
        
        place = data.get("city")

        if not place:
            raise ValueError("Can't determine the city by IP")

        self.home_coordinates = await asyncify(self.coordinates_from_name)(place)

        return self.home_coordinates

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
    

    @alru_cache
    async def get_places(self, place_name: str, radius_km: float | None = None) -> dict[str,PlaceInfo] | dict[str, Coordinates]:
        """
    
        
        :param place: name
        :type place: str
        :param radius_in_kilometers: search for objects within a radius (in kilometers)
        :type radius_in_kilometers: float
        :return: Dictionary of the format 'name: {full address:{distance,coordinates,opening hours}(PlaceInfo)'
        :rtype: Dict[str, PlaceInfo] | Dict[str, Coordinates]
        """
        await self.fetch_home_coordinates_if_needed()
        
        if not isinstance(self.home_coordinates, Coordinates):
            raise ValueError("Home location is not set")

        
        # TODO: cache
        # functools.cache
        # https://www.datacamp.com/tutorial/python-cache-introduction
        # lru cache
        # https://realpython.com/lru-cache-python/
        
    
        
        if radius_km is None:
            coords = self.coordinates_from_name(place_name)
            if coords is None:
                return {}
        
            place_info = PlaceInfo(Distance(0),coords,"не указано")

            return {place_name: place_info}
        
        home_lat = self.home_coordinates.latitude
        home_lon = self.home_coordinates.longitude
        lat_delta = radius_km / 111.0
        lon_delta = radius_km / (
            111.0 * math.cos(math.radians(home_lat))
        )

        viewbox = (
            Point(home_lat - lat_delta, home_lon - lon_delta),
            Point(home_lat + lat_delta, home_lon + lon_delta)
        )

        
        result = self.geolocator.geocode(
            query=f"{place_name}",
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
        matches_found[place_name] = {}
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
            
            
            place_info = PlaceInfo(distance,Coordinates(loc_lat, loc_lon),hours)
            
            matches_found[place_name][address] = place_info
        
        
        return dict(sorted(matches_found[place_name].items(),
                    key=lambda item: item[1].distance_km))
        
        