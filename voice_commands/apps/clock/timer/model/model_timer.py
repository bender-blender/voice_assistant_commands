from dataclasses import dataclass
from datetime import datetime


@dataclass
class TimerModel:
    target_time: datetime

    def return_seconds(self) -> int:
        delta = self.target_time - datetime.now()
        return int(delta.total_seconds())
