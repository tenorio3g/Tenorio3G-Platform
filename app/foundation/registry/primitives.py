# ==========================================================
# T3G-FND-005
#
# Element   : Primitives Registry
# Module    : Foundation UI
# Version   : 0.2.0
# Status    : Development
# Sprint    : FND-005.2
#
# Purpose
# -------
# Define el catálogo oficial de primitives disponibles
# dentro del T3G Framework.
#
# ==========================================================

from .enums import RegistryCategory, RegistryStatus
from .metadata import ComponentMetadata


PRIMITIVES = (
    ComponentMetadata(
        id="panel",
        name="Panel",
        category=RegistryCategory.PRIMITIVE,
        version="1.0.0",
        status=RegistryStatus.STABLE,
        since="0.1.0",
        owner="Foundation",
    ),
    ComponentMetadata(
        id="button",
        name="Button",
        category=RegistryCategory.PRIMITIVE,
        version="1.0.0",
        status=RegistryStatus.STABLE,
        since="0.1.0",
        owner="Foundation",
    ),
    ComponentMetadata(
        id="badge",
        name="Badge",
        category=RegistryCategory.PRIMITIVE,
        version="1.0.0",
        status=RegistryStatus.STABLE,
        since="0.1.0",
        owner="Foundation",
        
    ),
    ComponentMetadata(
        id="progress",
        name="Progress",
        category=RegistryCategory.PRIMITIVE,
        version="0.1.0",
        status=RegistryStatus.DEVELOPMENT,
        since="0.1.0",
        owner="Foundation",
    ),
    ComponentMetadata(
        id="avatar",
        name="Avatar",
        category=RegistryCategory.PRIMITIVE,
        status=RegistryStatus.PENDING,
        owner="Foundation",
    ),
    ComponentMetadata(
        id="icon",
        name="Icon",
        category=RegistryCategory.PRIMITIVE,
        status=RegistryStatus.PENDING,
        owner="Foundation",
    ),
)