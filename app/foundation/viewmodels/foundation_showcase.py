# ==========================================================
# T3G-FND-015
#
# Component : Foundation Showcase ViewModel
# Module    : Foundation UI
# Version   : 0.2.0
# Status    : Development
# Sprint    : FND-015
#
# Purpose
# -------
# Representa todos los datos preparados para la página
# Foundation Showcase.
#
# ==========================================================

from dataclasses import dataclass

from app.foundation.viewmodels.showcase_section import (
    ShowcaseSectionViewModel,
)


@dataclass(slots=True)
class FoundationShowcaseViewModel:
    """
    Modelo de presentación principal del catálogo visual
    de componentes Foundation.
    """

    title: str

    subtitle: str

    sections: tuple[ShowcaseSectionViewModel, ...]

    version: str = "0.2.0"

    status: str = "Development"

    @property
    def has_sections(self) -> bool:
        """
        Indica si existen componentes registrados
        para mostrar en el catálogo.
        """

        return bool(self.sections)

    @property
    def total_sections(self) -> int:
        """
        Devuelve la cantidad total de secciones visibles.
        """

        return sum(
            1
            for section in self.sections
            if section.visible
        )

    @property
    def visible_sections(
        self,
    ) -> tuple[ShowcaseSectionViewModel, ...]:
        """
        Devuelve únicamente las secciones visibles.
        """

        return tuple(
            section
            for section in self.sections
            if section.visible
        )