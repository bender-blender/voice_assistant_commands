from dataclasses import dataclass, field
from typing import Dict
import schedule


@dataclass
class AlarmModel:

    list_jobs: Dict[str, tuple[str, str, schedule.Job]] = field(default_factory=dict)

    def see_alarm(self):
        for k, v in self.list_jobs.items():
            print(f"{k} : {v[0]} {v[1]}")

    def cancel_alarm(self, name:str):
        if name in self.list_jobs:
            schedule.cancel_job(self.list_jobs[name][2])
            del self.list_jobs[name]
