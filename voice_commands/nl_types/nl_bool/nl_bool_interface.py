from abc import ABC, abstractmethod
from typing import Tuple

class NLBoolParseLanguage(ABC):
    def __init__(self, confirmations, rejections):
        self.confirmations = confirmations
        self.rejections = rejections


    def parse(self, from_string: str) -> Tuple[str,bool] | None:

        from_string = from_string.lower()
        if from_string in self.confirmations:
            return from_string, True

        if from_string in self.rejections:
            return from_string, False

        return None
