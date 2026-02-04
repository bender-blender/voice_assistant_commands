from stark.core.parsing import PatternParser, ObjectParser, Pattern, ParseError
from stark.core.commands_context import CommandsContext
from stark.general.classproperty import classproperty
from stark.core.parsing import RecognizedEntity
from stark.core.types import Object



from voice_commands.nl_types.nl_location.nl_location_implement import NLLocationImplement
from voice_commands.nl_types.parsing_context import pattern_parser
from utilits.gliner_processor import GliNERProcessor
from typing import cast



class NLLocation(Object):
    
    value: dict 
    loc_name: str

    @classproperty
    def pattern(self) -> Pattern:
        return Pattern("**")
    


class NLLocationParse(ObjectParser):

    def __init__(self, pattern_parser: PatternParser, home:str | None = None, radius_in_kilometers: float | None = None):
        self.pattern_parser = pattern_parser
        self.home = home
        self.radius_in_kilometers = radius_in_kilometers
        

    async def did_parse(self, obj:NLLocation, from_string:str):
        
        implement = NLLocationImplement(self.home)
        recognized_entities: list[RecognizedEntity] = []
        ner_processor = GliNERProcessor()
        await ner_processor.process_string(from_string,cast(CommandsContext,None),recognized_entities)
        if recognized_entities:
            place = " ".join([part.substring for part in recognized_entities])
            coordinates = await implement.resolve(place,self.radius_in_kilometers)
            obj.loc_name = place
            obj.value = coordinates
            #ner_processor.clear_recognized_entities(recognized_entities)
            return from_string
        
        raise ParseError("place not found")
        

        
pattern_parser.register_parameter_type(
    NLLocation, parser=NLLocationParse(pattern_parser))