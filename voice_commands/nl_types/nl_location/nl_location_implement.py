from typing import Dict
from voice_commands.providers.location_provider import LocationProvider,PlaceInfo,Coordinates


class NLLocationImplement:

    def __init__(self, home: str | None = None):
        self.provider = LocationProvider()
        self.home = home
    
    async def resolve(self, place: str, radius_in_kilometers: float | None = None) -> Dict[str,PlaceInfo] | Dict[str, Coordinates]:
        """
        Provide the user with the nearest points upon request
        """
        if self.provider.name_point is None:
            await self.provider.get_coordinates(self.home)
        
        mark = await self.provider._get_list_of_tags(place, radius_in_kilometers=radius_in_kilometers)
        return mark
        
    

