from abc import ABC,abstractmethod


class NLNumberParser(ABC):

    def __init__(self, pharse: str) -> None:
        self.pharse = pharse

    
    @abstractmethod
    def parse(self):
        pass