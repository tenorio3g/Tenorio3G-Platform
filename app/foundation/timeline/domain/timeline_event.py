from datetime import datetime
from uuid import uuid4


class TimelineEvent:

    def __init__(
        self,
        categoria,
        titulo,
        usuario,
        descripcion=None,
        icono="📄",
        color="gray",
        referencia=None,
        fecha=None,
        id=None
    ):
        self.id = id or str(uuid4())

        self.categoria = categoria
        self.titulo = titulo
        self.usuario = usuario
        self.descripcion = descripcion

        self.icono = icono
        self.color = color

        self.referencia = referencia

        self.fecha = fecha or datetime.now()