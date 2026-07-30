# ==========================================================
# T3G-FND-015
#
# Component : Showcase Section ViewModel
# Module    : Foundation UI
# Version   : 0.2.0
# Status    : Development
# Sprint    : FND-015
#
# Purpose
# -------
# Representa una sección del catálogo visual
# Foundation Showcase.
#
# ==========================================================

from dataclasses import (
    dataclass,
)


@dataclass(slots=True)
class ShowcaseSectionViewModel:
    """
    Modelo de presentación para una sección
    del Foundation Showcase.
    """

    title: str

    description: str

    component_name: str

    anchor: str

    visible: bool = True

    @property
    def id(self) -> str:
        """
        Identificador HTML de la sección.
        """

        return self.anchor.lower().replace(" ", "-")