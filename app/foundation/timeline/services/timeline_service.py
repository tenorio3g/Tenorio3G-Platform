from app.foundation.timeline.domain.timeline_event import TimelineEvent


class TimelineService:

    def registrar_evento(
        self,
        timeline,
        categoria,
        titulo,
        usuario,
        descripcion=None,
        icono="📄",
        color="gray",
        referencia=None,
        fecha=None
    ):
        if timeline is None:
            return None

        evento = TimelineEvent(
            categoria=categoria,
            titulo=titulo,
            usuario=usuario,
            descripcion=descripcion,
            icono=icono,
            color=color,
            referencia=referencia,
            fecha=fecha
        )

        agregado = timeline.agregar_evento(evento)

        if not agregado:
            return None

        return evento