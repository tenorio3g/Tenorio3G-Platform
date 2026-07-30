from datetime import datetime


class WorkOrderMaterial:

    def __init__(
        self,
        nombre,
        cantidad,
        unidad,
        codigo=None,
        marca=None,
        descripcion=None,
        observaciones=None,
        costo_unitario=0
    ):
        self.nombre = str(nombre or "").strip()
        self.unidad = str(unidad or "").strip()

        self.codigo = (
            str(codigo).strip()
            if codigo is not None
            else None
        )

        self.marca = (
            str(marca).strip()
            if marca is not None
            else None
        )

        self.descripcion = (
            str(descripcion).strip()
            if descripcion is not None
            else None
        )

        self.observaciones = (
            str(observaciones).strip()
            if observaciones is not None
            else None
        )

        if not self.nombre:
            raise ValueError(
                "El nombre del material es obligatorio."
            )

        if not self.unidad:
            raise ValueError(
                "La unidad del material es obligatoria."
            )

        try:
            self.cantidad = float(cantidad)
        except (TypeError, ValueError):
            raise ValueError(
                "La cantidad debe ser un número válido."
            )

        if self.cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        try:
            self.costo_unitario = float(costo_unitario or 0)
        except (TypeError, ValueError):
            raise ValueError(
                "El costo unitario debe ser un número válido."
            )

        if self.costo_unitario < 0:
            raise ValueError(
                "El costo unitario no puede ser negativo."
            )

        self.fecha_registro = datetime.now()

    @property
    def costo_total(self):
        return self.cantidad * self.costo_unitario

    def aumentar_cantidad(self, cantidad):
        try:
            cantidad = float(cantidad)
        except (TypeError, ValueError):
            raise ValueError(
                "La cantidad debe ser un número válido."
            )

        if cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        self.cantidad += cantidad

    def disminuir_cantidad(self, cantidad):
        try:
            cantidad = float(cantidad)
        except (TypeError, ValueError):
            raise ValueError(
                "La cantidad debe ser un número válido."
            )

        if cantidad <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

        if cantidad > self.cantidad:
            raise ValueError(
                "La cantidad no puede quedar negativa."
            )

        self.cantidad -= cantidad