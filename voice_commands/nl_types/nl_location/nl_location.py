from stark.core.parsing import PatternParser, ObjectParser, Pattern, ParseError
from stark.general.classproperty import classproperty
from stark.core.types import Object


from voice_commands.nl_types.nl_location.nl_location_implement import NLLocationProvider
from voice_commands.nl_types.parsing_context import pattern_parser

from voice_commands.providers.location_provider import LocationProvider,PlaceInfo,Coordinates

# type Kilometer = float

class NLLocation(Object):
    
    value: str
    places: dict[str,PlaceInfo] | dict[str, Coordinates]
    provider = LocationProvider()

    @classproperty
    def pattern(self) -> Pattern:
        return Pattern("**")
    
    async def set_home(self, home:str | None = None):
        await self.provider.fetch_home_coordinates_if_needed(home)
        
    async def resolve(self, place: str, radius_km: float = 10) -> dict[str, PlaceInfo] | dict[str, Coordinates]:
        """
        Provide the user with the nearest points upon request
        """
        
        mark = await self.provider.get_places(place, radius_km=radius_km)
        return mark
    
    async def did_parse(self, from_string: str):
        
        coordinates = await self.resolve(from_string)
        self.places = coordinates
        self.value = from_string
        return from_string



        
pattern_parser.register_parameter_type(
    NLLocation)