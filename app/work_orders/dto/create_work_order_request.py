class CreateWorkOrderRequest:

    def __init__(
        self,
        numero,
        titulo,
        descripcion,
        tipo,
        prioridad,
        codigo_activo,
        numero_solicitante,
        numero_supervisor
    ):
        self.numero = numero
        self.titulo = titulo
        self.descripcion = descripcion
        self.tipo = tipo
        self.prioridad = prioridad
        self.codigo_activo = codigo_activo
        self.numero_solicitante = numero_solicitante
        self.numero_supervisor = numero_supervisor