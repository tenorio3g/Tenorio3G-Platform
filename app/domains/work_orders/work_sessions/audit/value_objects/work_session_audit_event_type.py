from enum import Enum


class WorkSessionAuditEventType(
    str,
    Enum,
):

    MANUAL_CREATED = "MANUAL_CREATED"

    CORRECTED = "CORRECTED"
