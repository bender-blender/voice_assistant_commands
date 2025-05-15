from .Info import Info
from uuid import UUID


class Hour(Info):
    id: UUID
    hour_index: int
    day_id: UUID
