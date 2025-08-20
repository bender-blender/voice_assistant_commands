from dataclasses import dataclass, field
from typing import Dict,List
import schedule


@dataclass
class AlarmModel:

    list_jobs: Dict[str, List[tuple[str, str, schedule.Job]]] = field(default_factory=dict)

    def see_alarm(self):
        return self.list_jobs

    def cancel_alarm(self, name:str):
        if name in self.list_jobs:
            for job in self.list_jobs[name]:
                if job[2] is not None:
                    schedule.cancel_job(job[2])
            del self.list_jobs[name]
