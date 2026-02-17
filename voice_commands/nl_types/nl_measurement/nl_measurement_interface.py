from abc import ABC, abstractmethod
from pint import UnitRegistry
from typing import Dict

class MeasurementParseInterface(ABC):

    def __init__(self) -> None:
        self.dictionary_quantities:Dict[str,float] = {}
    

    @abstractmethod
    def parse(self, from_string: str) -> UnitRegistry | None:
        pass


