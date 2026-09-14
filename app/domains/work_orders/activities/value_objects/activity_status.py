from enum import Enum


class ActivityStatus(str, Enum):

    PENDING = "PENDING"

    IN_PROGRESS = "IN_PROGRESS"

    ON_HOLD = "ON_HOLD"

    COMPLETED = "COMPLETED"
