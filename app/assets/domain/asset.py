from app.assets.domain.asset_event import AssetEvent
from app.assets.domain.asset_photo import AssetPhoto
from app.shared.constants import AssetStatus


class Asset:
    """
    Representa un activo industrial dentro de Tenorio3G.

    La clase contiene únicamente información y reglas de negocio
    relacionadas con el activo. No conoce Flask, bases de datos,
    formularios, rutas ni elementos de la interfaz gráfica.
    """

    def __init__(
        self,
        codigo,
        nombre,
        estado,
        ubicacion,
        area,
        salud,
        ultimo_mantenimiento,
        proximo_mantenimiento,
        events=None,
        photos=None,
    ):
        self.codigo = codigo
        self.nombre = nombre
        self.estado = estado
        self.ubicacion = ubicacion
        self.area = area
        self.salud = salud
        self.ultimo_mantenimiento = ultimo_mantenimiento
        self.proximo_mantenimiento = proximo_mantenimiento

        # Se crean listas independientes para evitar compartir
        # accidentalmente colecciones entre diferentes activos.
        self.events = list(events) if events else []
        self.photos = list(photos) if photos else []

    # ==================================================
    # Acciones relacionadas con eventos
    # ==================================================

    def agregar_evento(
        self,
        title,
        description,
        event_type,
        created_by,
    ):
        """
        Crea y agrega un evento al historial del activo.

        Returns:
            El evento creado.
        """

        event = AssetEvent(
            title=title,
            description=description,
            event_type=event_type,
            created_by=created_by,
        )

        self.events.append(event)

        return event

    # ==================================================
    # Acciones relacionadas con fotografías
    # ==================================================

    def agregar_fotografia(
        self,
        image_path,
        description,
        photo_type,
        created_by,
        is_primary=False,
    ):
        """
        Crea y agrega una fotografía al activo.

        Cuando la fotografía se marca como principal, cualquier otra
        fotografía principal registrada anteriormente deja de serlo.

        Args:
            image_path: Ruta o referencia de la imagen.
            description: Descripción de lo que muestra la fotografía.
            photo_type: Clasificación de la fotografía.
            created_by: Persona que registró la evidencia.
            is_primary: Indica si será la imagen principal del activo.

        Returns:
            La fotografía creada.
        """

        if is_primary:
            self._desmarcar_fotografia_principal()

        photo = AssetPhoto(
            image_path=image_path,
            description=description,
            photo_type=photo_type,
            created_by=created_by,
            is_primary=is_primary,
        )

        self.photos.append(photo)

        return photo

    def establecer_fotografia_principal(self, photo):
        """
        Establece una fotografía existente como imagen principal.

        Args:
            photo: Fotografía perteneciente al activo.

        Returns:
            True si la fotografía pudo establecerse como principal.
            False si no pertenece al activo.
        """

        if photo not in self.photos:
            return False

        self._desmarcar_fotografia_principal()
        photo.is_primary = True

        return True

    def _desmarcar_fotografia_principal(self):
        """
        Elimina la condición de principal de todas las fotografías.
        """

        for photo in self.photos:
            photo.is_primary = False

    # ==================================================
    # Consultas relacionadas con eventos
    # ==================================================

    def tiene_eventos(self):
        """
        Indica si el activo tiene eventos registrados.
        """

        return bool(self.events)

    def cantidad_eventos(self):
        """
        Devuelve la cantidad de eventos registrados.
        """

        return len(self.events)

    def ultimo_evento(self):
        """
        Devuelve el último evento registrado.

        Returns:
            El último evento o None cuando no existen eventos.
        """

        if not self.events:
            return None

        return self.events[-1]

    # ==================================================
    # Consultas relacionadas con fotografías
    # ==================================================

    def tiene_fotografias(self):
        """
        Indica si el activo tiene fotografías registradas.
        """

        return bool(self.photos)

    def cantidad_fotografias(self):
        """
        Devuelve la cantidad de fotografías registradas.
        """

        return len(self.photos)

    def fotografia_principal(self):
        """
        Devuelve la fotografía principal del activo.

        Si ninguna fotografía está marcada como principal, devuelve
        la primera fotografía disponible.

        Returns:
            La fotografía principal, la primera disponible o None.
        """

        for photo in self.photos:
            if photo.is_primary:
                return photo

        if self.photos:
            return self.photos[0]

        return None

    def fotografias_por_tipo(self, photo_type):
        """
        Devuelve las fotografías que pertenecen a un tipo determinado.

        Args:
            photo_type: Tipo de fotografía que se desea consultar.

        Returns:
            Lista de fotografías coincidentes.
        """

        if not isinstance(photo_type, str):
            return []

        normalized_type = photo_type.strip().lower()

        if not normalized_type:
            return []

        return [
            photo
            for photo in self.photos
            if isinstance(photo.photo_type, str)
            and photo.photo_type.strip().lower() == normalized_type
        ]

    # ==================================================
    # Consultas generales del activo
    # ==================================================

    def esta_operando(self):
        """
        Indica si el activo se encuentra operando.
        """

        return self.estado == AssetStatus.OPERANDO

    def necesita_mantenimiento(self):
        """
        Determina si la salud del activo requiere mantenimiento.
        """

        return isinstance(self.salud, (int, float)) and self.salud < 70

    def salud_color(self):
        """
        Devuelve una clasificación visual de la salud del activo.
        """

        if not isinstance(self.salud, (int, float)):
            return "neutral"

        if self.salud >= 90:
            return "success"

        if self.salud >= 70:
            return "warning"

        return "danger"

    def resumen(self):
        """
        Devuelve un resumen corto del activo.
        """

        return f"{self.nombre} ({self.codigo})"