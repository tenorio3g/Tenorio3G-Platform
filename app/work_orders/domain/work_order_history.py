from datetime import datetime


class WorkOrderHistory:

    def __init__(
        self,
        estado_anterior,
        estado_nuevo,
        usuario,
        comentario=None,
        fecha=None
    ):
        self.estado_anterior = estado_anterior
        self.estado_nuevo = estado_nuevo
        self.usuario = usuario
        self.comentario = comentario
        self.fecha = fecha or datetime.now()