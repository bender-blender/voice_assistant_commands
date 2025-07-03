from ....providers.location_provider import LocationProvider
from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from dataclasses import dataclass


@dataclass
class Location(Object):

    coord: String


    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$coord:String")

    async def did_parse(self, from_string: str) -> str:
        location = LocationProvider()
        if not from_string:
            raise ParseError("Город не указан")
        
        part_line = from_string.split(" ")
        while True:
            line = " ".join(part_line)
            try:
                place = location.get_coordinates(line)
                self.value = place
                self.coord = self.value
                break
            except ValueError:
                part_line.pop(0)
        
        return from_string

Pattern.add_parameter_type(Location)