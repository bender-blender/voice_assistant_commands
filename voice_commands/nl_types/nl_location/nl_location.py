from stark.core.parsing import PatternParser, ObjectParser, Pattern, ParseError
from stark.core.commands_context import CommandsContext
from stark.general.classproperty import classproperty
from stark.core.parsing import RecognizedEntity
from stark.core.types import Object



from voice_commands.nl_types.nl_location.nl_location_implement import NLLocationImplement
from voice_commands.nl_types.parsing_context import pattern_parser
from utilits.gliner_processor import GliNERProcessor
from typing import cast

from voice_commands.providers.location_provider import LocationProvider


# type Kilometer = float

class NLLocation(Object):
    
    value: dict 
    loc_name: str

    @classproperty
    def pattern(self) -> Pattern:
        return Pattern("**")
    
    async def resolve(self, place: str, radius_km: float | None = None) -> dict[str, PlaceInfo] | dict[str, Coordinates]:
        """
        Provide the user with the nearest points upon request
        """
        
        provider = LocationProvider()
        mark = await provider.get_places(place, radius_km=radius_km)
        return mark

# Parse - verb, to parse. I want to parse a string. def parse_html()
# Parser - who parses. I want to create a parser for a string.
# parsed - result of parsing. I want to get a parsed string.

# def get_taxi(location: NLLocation):
#     location.resolve(radius_in_kilometers=10)

class NLLocationParser(ObjectParser):

    def __init__(self, pattern_parser: PatternParser, home:str | None = None, radius_in_kilometers: float | None = None):
        self.pattern_parser = pattern_parser
        self.home = home
        self.radius_in_kilometers = radius_in_kilometers
        

    async def did_parse(self, obj: NLLocation, from_string: str):
        
        implement = NLLocationImplement(self.home)
        # recognized_entities: list[RecognizedEntity] = []
        # NOTE: register in the def run
        # https://github.com/MarkParker5/STARK/blob/master/stark/__init__.py
        # ner_processor = GliNERProcessor()
        # await ner_processor.process_string(from_string,cast(CommandsContext,None),recognized_entities)
        # if recognized_entities:
        # place = " ".join([part.substring for part in recognized_entities])
        coordinates = await implement.resolve(from_string, self.radius_in_kilometers)
        obj.loc_name = from_string
        obj.value = coordinates
        #ner_processor.clear_recognized_entities(recognized_entities)
        return from_string
        
        raise ParseError("place not found")
        

        
pattern_parser.register_parameter_type(
    NLLocation, parser=NLLocationParser(pattern_parser))