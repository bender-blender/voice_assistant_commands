from uuid import UUID

from .Info import Info


class Hour(Info):
    id: UUID

    hour_index: int

    day_id: UUID
