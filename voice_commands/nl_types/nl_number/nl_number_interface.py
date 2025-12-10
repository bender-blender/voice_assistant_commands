from typing import Tuple,Protocol

class NLNumberParseWordToNum(Protocol):
    def parse(self, pharse:str) -> Tuple[float, bool] | None:
        pass


class NLNumberParserDucklingTranslated(Protocol):
    def parse(self, pharse: str) -> Tuple[float, bool] | None:
        pass


class NLNumberParseCustom(Protocol):
    def parse(self, pharse: str) -> Tuple[float, bool] | None:
        pass

    def _get_fraction(self, list_num: list[int | float], pharse: list[str]) -> str | None:
        pass

    def _get_part(self, list_num: list[int | float], pharse: list[str]) -> float | None:
        pass


    def _get_half(self, list_num: list[int | float], pharse: list[str]) -> float | None:
        pass
