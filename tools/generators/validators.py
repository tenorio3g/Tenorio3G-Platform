from __future__ import annotations


class ModuleNameValidator:
    """
    Valida nombres de módulos para el Tool Framework de Tenorio3G.
    """

    MIN_LENGTH = 3
    MAX_LENGTH = 40

    @classmethod
    def validate(
        cls,
        module_name: str,
    ) -> None:
        """
        Valida el nombre recibido.

        Raises:
            TypeError:
                Si el valor no es texto.
            ValueError:
                Si incumple alguna regla de nomenclatura.
        """

        if not isinstance(module_name, str):
            raise TypeError(
                "Module name must be a string."
            )

        if not module_name:
            raise ValueError(
                "Module name cannot be empty."
            )

        if len(module_name) < cls.MIN_LENGTH:
            raise ValueError(
                "Module name must contain at least 3 characters."
            )

        if len(module_name) > cls.MAX_LENGTH:
            raise ValueError(
                "Module name cannot exceed 40 characters."
            )

        if not module_name[0].isupper():
            raise ValueError(
                "Module name must start with an uppercase letter."
            )

        if not module_name.isalpha():
            raise ValueError(
                "Module name may contain only alphabetic characters."
            )