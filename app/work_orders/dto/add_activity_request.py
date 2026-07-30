class AddActivityRequest:

    def __init__(
        self,
        numero_orden,
        titulo,
        descripcion,
        numero_responsable,
        usuario
    ):
        self.numero_orden = numero_orden
        self.titulo = titulo
        self.descripcion = descripcion
        self.numero_responsable = numero_responsable
        self.usuario = usuario