from typing import Dict
from voice_commands.providers.location_provider import LocationProvider,PlaceInfo,Coordinates


class NLLocationProvider:

    def __init__(self, home: str | None = None):
        self.provider = LocationProvider()
        self.home = home
    
    async def resolve(self, place: str, radius_in_kilometers: float | None = None) -> Dict[str,PlaceInfo] | Dict[str, Coordinates]:
        """
        Provide the user with the nearest points upon request
        """
        mark = await self.provider.get_places(place, radius_km=radius_in_kilometers)
        return mark
        
    

