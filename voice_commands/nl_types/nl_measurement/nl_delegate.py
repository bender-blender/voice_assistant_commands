from voice_commands.nl_types.nl_measurement.nl_measurement_implementation import (
    MeasurementParseRu,
    MeasurementParseEn
)

from voice_commands.nl_types.nl_measurement.nl_measurement_interface import MeasurementParseInterface
from voice_commands.helpers.detect_lang import identify_the_language
from stark.core.parsing import ParseError
from pint import UnitRegistry


class MeasurmentDelegate:

    def __init__(self) -> None:
        self.language_parsers:dict[str,MeasurementParseInterface] = {"ru":MeasurementParseRu(),"en":MeasurementParseEn()}

    
    def parse(self, from_string:str) -> UnitRegistry | None:
        lang = identify_the_language(from_string)
        if not lang:
            raise ParseError(f'Unsupported language: {lang}')

        parsers = self.language_parsers.get(lang)

        if not parsers:
            raise ParseError(f'Unsupported language: {lang}')

        
        parsing_stages = parsers.parse(from_string)
        if parsing_stages:
            return parsing_stages
        return None

