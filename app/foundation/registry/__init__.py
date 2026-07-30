# ==========================================================
# T3G-FND-005
#
# Element   : Foundation Registry
# Module    : Foundation UI
# Version   : 0.1.0
# Status    : Development
# Sprint    : FND-005
#
# Purpose
# -------
# Expone públicamente los catálogos de primitives y
# componentes de Foundation UI.
#
# ==========================================================

from .components import COMPONENTS
from .enums import RegistryCategory, RegistryStatus
from .metadata import ComponentMetadata
from .primitives import PRIMITIVES
from .service import RegistryService
from .validator import (
    RegistryValidationError,
    RegistryValidator,
)

__all__ = [
    "COMPONENTS",
    "ComponentMetadata",
    "PRIMITIVES",
    "RegistryCategory",
    "RegistryService",
    "RegistryStatus",
    "RegistryValidationError",
    "RegistryValidator",
]