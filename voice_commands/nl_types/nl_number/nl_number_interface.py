from typing import Tuple,Protocol
from voice_commands.nl_types.nl_number.parse_duckling import Number

class NLNumberParseWordToNum(Protocol):
    def parse(self, pharse:str) -> Tuple[Number, str] | None:
        pass


class NLNumberParserDucklingTranslated(Protocol):
    def parse(self, pharse: str) -> Tuple[Number, str] | None:
        pass


class NLNumberParseCustom(Protocol):
    def parse(self, pharse: str) -> Tuple[Number, str] | None:
        pass

    def _get_fraction(self, list_num: list[int | float], pharse: list[str]) -> str | None:
        pass

    def _get_part(self, list_num: list[int | float], pharse: list[str]) -> float | None:
        pass


    def _get_half(self, list_num: list[int | float], pharse: list[str]) -> float | None:
        pass