from __future__ import annotations

from enum import Enum


class WorkOrderStatus(str, Enum):

    CREATED = "CREATED"

    APPROVED = "APPROVED"

    ASSIGNED = "ASSIGNED"

    IN_PROGRESS = "IN_PROGRESS"

    ON_HOLD = "ON_HOLD"

    COMPLETED = "COMPLETED"

    CLOSED = "CLOSED"

    CANCELLED = "CANCELLED"
