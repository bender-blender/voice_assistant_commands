from ....providers.location_provider import LocationProvider, Coordinates
from stark.general.classproperty import classproperty
from stark.core.types import Object, ParseError
from stark.core.patterns import Pattern



class Location(Object):
    value: Coordinates | None = None
    
    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    async def did_parse(self, from_string) -> str:
        location_provider = LocationProvider()
        print(from_string)
        words = from_string.replace("-"," ").split(" ")
        count_words = len(words)
        substring = []
        for i in range(count_words):
            for j in range(i+1, count_words):
                substring.append(words[i:j])
        
        substring_dictionary = {}
        for sub in substring:
            substring_dictionary[" ".join(
                sub)] = location_provider.get_coordinates(" ".join(sub))
        
        print(substring_dictionary)

        self.value = Coordinates(42,23)
        return from_string

Pattern.add_parameter_type(Location)