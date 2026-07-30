class WorkOrderTool:

    def __init__(
        self,
        nombre,
        cantidad=1,
        codigo=None,
        observaciones=None
    ):
        self.nombre = nombre
        self.cantidad = cantidad
        self.codigo = codigo
        self.observaciones = observaciones