from typing import List


from datetime import datetime


from uuid import UUID


from .Info import Info


from .Hour import Hour


class Day(Info):

    id: UUID

    hours: List[Hour]

    date: datetime
