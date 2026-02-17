from stark.core.parsing import PatternParser, ObjectParser, Pattern
from stark.general.classproperty import classproperty
from stark.core.parsing import ParseError
from stark.core.parsing import Object
from fb_duckling import Duckling


from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_number.nl_number import NLNumber
from voice_commands.nl_types.nl_measurement.nl_unit import NLUnit
from voice_commands.helpers.detect_lang import identify_the_language
from voice_commands.nl_types.nl_measurement.units import Quantity


class NLMeasurement(Object):

    value: Quantity
    number: NLNumber
    unit: NLUnit

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("($number:NLNumber $unit:NLUnit|**)")


class NLMeasurementParse(ObjectParser):
    def __init__(self, pattern_parser: PatternParser):
        self.pattern_parser = pattern_parser

    async def did_parse(self, obj: NLMeasurement, from_string: str) -> str:
        try:
            obj.value = Quantity(obj.number.value, obj.unit.value)
            return from_string
        except AttributeError:
            pass

        lang_code = {"ru": "ru_RU", "en": "en_US"}
        lang_text = identify_the_language(from_string)

        if lang_text is None or lang_text not in lang_code:
            lang_text = "en"

        duckling = Duckling(locale=lang_code[lang_text])


        parse = duckling(from_string)

        if parse:
            result = parse[0]
            value = result["value"]["value"]
            unit = result["value"]["unit"]
            if value is not None and unit is not None:
                obj.number = value
                obj.unit = unit
                obj.value = Quantity(obj.number, obj.unit)
                return from_string

        raise ParseError("physical quantity not found")


pattern_parser.register_parameter_type(
    NLMeasurement, parser=NLMeasurementParse(pattern_parser))
