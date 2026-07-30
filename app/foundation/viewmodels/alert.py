# ==========================================================
# T3G-FND-014
#
# Component : Alert ViewModel
# Module    : Foundation UI
# Version   : 0.2.0
# Status    : Development
# Sprint    : FND-014
#
# Purpose
# -------
# Representa un mensaje reutilizable de información,
# éxito, advertencia o error.
#
# ==========================================================

from dataclasses import (
    dataclass,
)


@dataclass(slots=True)
class AlertViewModel:
    """
    Modelo de presentación para el componente Alert.
    """

    title: str

    message: str

    type: str = "info"

    icon: str = "ℹ️"

    dismissible: bool = False

    visible: bool = True