class AddMaterialRequest:

    def __init__(
        self,
        numero_orden,
        nombre,
        cantidad,
        unidad,
        usuario,
        codigo=None,
        marca=None,
        descripcion=None,
        observaciones=None,
        costo_unitario=0
    ):
        self.numero_orden = numero_orden
        self.nombre = nombre
        self.cantidad = cantidad
        self.unidad = unidad
        self.usuario = usuario

        self.codigo = codigo
        self.marca = marca
        self.descripcion = descripcion
        self.observaciones = observaciones
        self.costo_unitario = costo_unitario