from enum import Enum


class ActivityStatus(str, Enum):

    PENDING = "PENDING"

    IN_PROGRESS = "IN_PROGRESS"

    COMPLETED = "COMPLETED"