from enum import Enum


class ToolUsageStatus(str, Enum):

    ISSUED = "ISSUED"
    RETURNED = "RETURNED"