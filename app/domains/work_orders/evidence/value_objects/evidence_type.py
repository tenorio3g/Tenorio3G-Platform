from enum import Enum


class EvidenceType(str, Enum):

    BEFORE_PHOTO = "BEFORE_PHOTO"
    AFTER_PHOTO = "AFTER_PHOTO"
    MEASUREMENT = "MEASUREMENT"
    DOCUMENT = "DOCUMENT"
    OTHER = "OTHER"