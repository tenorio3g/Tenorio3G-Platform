from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssetLifeSheetViewModel:
    """
    ViewModel para la Hoja de Vida de un Activo.

    Este objeto representa exclusivamente la información que la interfaz
    necesita mostrar. No contiene lógica de negocio.
    """

    codigo: str
    nombre: str
    estado: str
    ubicacion: str
    area: str
    modelo: str
    salud: int

    ultimo_mantenimiento: str | None
    proximo_mantenimiento: str | None