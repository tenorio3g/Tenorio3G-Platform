from datetime import datetime


class AssetPhoto:
    """
    Representa una evidencia fotográfica de un activo.
    """

    def __init__(
        self,
        image_path,
        description,
        photo_type,
        created_by,
        is_primary=False,
        created_at=None,
    ):
        self.image_path = image_path
        self.description = description
        self.photo_type = photo_type
        self.created_by = created_by
        self.is_primary = is_primary
        self.created_at = created_at or datetime.now()

    def marcar_como_principal(self):
        """
        Marca esta fotografía como principal.
        """
        self.is_primary = True

    def quitar_como_principal(self):
        """
        Quita el estado de fotografía principal.
        """
        self.is_primary = False

    def resumen(self):
        """
        Devuelve un resumen de la fotografía.
        """
        return f"{self.photo_type} - {self.description}"