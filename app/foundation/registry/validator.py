# ==========================================================
# T3G-FND-009
#
# Element   : Registry Validator
# Module    : Foundation Registry
# Version   : 0.2.0
# Status    : Development
# Sprint    : FND-005.6
#
# Purpose
# -------
# Valida la integridad estructural del Registry
# perteneciente al T3G Framework.
#
# ==========================================================

from .service import RegistryService


class RegistryValidationError(Exception):
    """
    Error específico de validación del Registry.
    """


class RegistryValidator:
    """
    Audita la integridad del catálogo oficial
    del T3G Framework.
    """

    def __init__(self) -> None:
        self.registry = RegistryService()

    def validate(self) -> None:
        """
        Ejecuta todas las reglas de validación.
        """

        self.validate_unique_ids()
        self.validate_dependencies()
        self.validate_circular_dependencies()

    def validate_unique_ids(self) -> None:
        """
        Verifica que ningún elemento comparta el mismo id.
        """

        registered_ids: set[str] = set()

        for item in self.registry.all:
            if item.id in registered_ids:
                raise RegistryValidationError(
                    f"Registry contiene un id duplicado: '{item.id}'."
                )

            registered_ids.add(item.id)

    def validate_dependencies(self) -> None:
        """
        Verifica que todas las dependencias declaradas existan.
        """

        registered_ids = {
            item.id
            for item in self.registry.all
        }

        for item in self.registry.all:
            for dependency in item.depends_on:
                if dependency not in registered_ids:
                    raise RegistryValidationError(
                        f"'{item.id}' depende de '{dependency}', "
                        "pero esa dependencia no existe."
                    )

    def validate_circular_dependencies(self) -> None:
        """
        Verifica que el Registry no contenga ciclos
        entre sus dependencias.
        """

        dependency_graph = {
            item.id: item.depends_on
            for item in self.registry.all
        }

        visited: set[str] = set()
        active_path: set[str] = set()

        def visit(component_id: str, path: list[str]) -> None:
            if component_id in active_path:
                cycle_start = path.index(component_id)
                cycle = path[cycle_start:] + [component_id]

                raise RegistryValidationError(
                    "Dependencia circular detectada: "
                    + " -> ".join(cycle)
                )

            if component_id in visited:
                return

            active_path.add(component_id)
            path.append(component_id)

            for dependency in dependency_graph[component_id]:
                visit(dependency, path)

            path.pop()
            active_path.remove(component_id)
            visited.add(component_id)

        for component_id in dependency_graph:
            if component_id not in visited:
                visit(component_id, [])