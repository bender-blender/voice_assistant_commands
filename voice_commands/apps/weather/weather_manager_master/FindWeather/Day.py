from datetime import datetime
from typing import List
from uuid import UUID

from .Hour import Hour
from .Info import Info


class Day(Info):
    id: UUID

    hours: List[Hour]

    date: datetime
