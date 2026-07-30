from datetime import datetime


class WorkOrderEvent:

    def __init__(
        self,
        tipo,
        titulo,
        usuario,
        descripcion=None,
        fecha=None
    ):
        self.tipo = tipo
        self.titulo = titulo
        self.usuario = usuario
        self.descripcion = descripcion
        self.fecha = fecha or datetime.now()