from dataclasses import dataclass
from datetime import datetime


@dataclass
class TimerModel:
    target_time: datetime

    def return_seconds(self) -> int:
        delta = self.target_time - datetime.now()
        return max(0, int(delta.total_seconds()))  # not sure negative seconds should be cut
