from stark.core.parsing import Pattern
from stark.general.classproperty import classproperty
from stark.core.parsing import ParseError
from stark.core.parsing import Object

from voice_commands.nl_types.nl_measurement.nl_unit import NLAbstractUnit
from voice_commands.nl_types.nl_measurement.units import Quantity
from voice_commands.nl_types.nl_number.nl_number import NLNumber



class NLMeasurement(Object):

    value: Quantity
    number: NLNumber
    unit: NLAbstractUnit
    _unit_type:type[NLAbstractUnit]

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern(f"$number:NLNumber $unit:{cls._unit_type.__name__}")
    
    async def did_parse(self,  from_string: str) -> str:
        if self.number is None or self.unit is None:
            raise ParseError("Measurement not found")
    
        self.value = Quantity(self.number.value, self.unit.value)
        return from_string

