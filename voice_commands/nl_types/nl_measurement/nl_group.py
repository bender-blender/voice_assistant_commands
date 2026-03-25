from stark.general.classproperty import classproperty
from stark.core.parsing import ParseError
from stark.core.parsing import Pattern
from stark.core.parsing import Object


from voice_commands.nl_types.nl_measurement.nl_measurement import NLMeasurement
from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_measurement.units import Quantity
from voice_commands.nl_types.parsing_context import pattern_parser



class Group(Object):

    _types:list[type[NLMeasurement]]
    value: Quantity
    
    measurement: type[NLMeasurement]
    pattern_dict:dict[str,str] = {}
    

    @classmethod
    def __create_parameter_dict(cls):
        n = 1
        for i in cls._types:
            parameter_signature = f"$measurement{n}:"
            cls.pattern_dict[parameter_signature] = i.__name__
            n += 1
    
    @classmethod
    def __create_pattern(cls):
        if not cls.pattern_dict:
            raise ValueError("pattern_dict is empty")

        parts = [f"{key}{value}" for key, value in cls.pattern_dict.items()]
        return "(" + "|".join(parts) + ")"
    

    @classproperty
    def pattern(cls) -> Pattern:
        cls.__create_parameter_dict()
        pattern = cls.__create_pattern()
        print(pattern)
        return Pattern(f"{pattern}")
    
    async def did_parse(self, from_string):
        print(f"Substring NLGroup -> {from_string}")
        for key,value in self.__dict__.items():
            if value is not None and key.startswith("measurement"):
                setattr(self,key,value)
                self.value = value
                return from_string
        raise ParseError("Group not found")

    
pattern_parser.register_parameter_type(Group)

