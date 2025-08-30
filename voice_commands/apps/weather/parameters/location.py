import anyio
from stark.core.patterns import Pattern
from stark.core.types import Object, ParseError
from stark.general.classproperty import classproperty

from utilits.combinatorics import async_combinatorics

from voice_commands.providers.location_provider import Coordinates, LocationProvider
from typing import Optional, Tuple

class Location(Object):
    value: Coordinates | None = None
    location_provider = LocationProvider()

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    async def did_parse(self, from_string: str) -> str:
        # Optimization: use offline geo names library at least for pre-validation

        res:Optional[Tuple[str, Optional[Coordinates]]] = await async_combinatorics(from_string, self.location_provider.get_coordinates, True, min_delay_sec=1.1)
        await anyio.sleep(0.000001)
        if res is None:
            raise ParseError("Не удалось определить местоположение.")

        subst, self.value = res

        if self.value is None:
            raise ParseError("failed to parse location")

        return subst


Pattern.add_parameter_type(Location)
