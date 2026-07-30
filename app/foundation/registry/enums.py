# ==========================================================
# T3G-FND-008
#
# Element   : Registry Enums
# Module    : Foundation Registry
# Version   : 0.1.0
# Status    : Development
# Sprint    : FND-005.4
#
# Purpose
# -------
# Define los valores oficiales permitidos para estados
# y categorías del Registry del T3G Framework.
#
# ==========================================================

from enum import Enum


class RegistryStatus(str, Enum):
    """
    Estados permitidos para los elementos del Registry.
    """

    PENDING = "pending"
    DEVELOPMENT = "development"
    STABLE = "stable"
    DEPRECATED = "deprecated"


class RegistryCategory(str, Enum):
    """
    Categorías oficiales del T3G Framework.
    """

    PRIMITIVE = "primitive"
    COMPONENT = "component"
    PATTERN = "pattern"
    UTILITY = "utility"