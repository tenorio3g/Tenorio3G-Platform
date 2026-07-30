from app.work_orders.domain.work_order_material import (
    WorkOrderMaterial
)

from app.work_orders.dto.add_material_request import (
    AddMaterialRequest
)

from app.work_orders.repositories.work_order_repository import (
    WorkOrderRepository
)


class AddMaterialService:

    def __init__(self, work_order_repository=None):
        self.work_order_repository = (
            work_order_repository
            or WorkOrderRepository()
        )

    def ejecutar(self, request):

        if not isinstance(request, AddMaterialRequest):
            raise TypeError(
                "Se esperaba un objeto AddMaterialRequest."
            )

        numero_orden = str(
            request.numero_orden or ""
        ).strip()

        nombre = str(
            request.nombre or ""
        ).strip()

        unidad = str(
            request.unidad or ""
        ).strip()

        usuario = str(
            request.usuario or ""
        ).strip()

        if not numero_orden:
            raise ValueError(
                "El número de orden es obligatorio."
            )

        if not nombre:
            raise ValueError(
                "El nombre del material es obligatorio."
            )

        if not unidad:
            raise ValueError(
                "La unidad del material es obligatoria."
            )

        if not usuario:
            raise ValueError(
                "El usuario que registra el material es obligatorio."
            )

        orden = (
            self.work_order_repository
            .obtener_por_numero(numero_orden)
        )

        if orden is None:
            raise ValueError(
                f"No existe la orden '{numero_orden}'."
            )

        material = WorkOrderMaterial(
            nombre=nombre,
            cantidad=request.cantidad,
            unidad=unidad,
            codigo=request.codigo,
            marca=request.marca,
            descripcion=request.descripcion,
            observaciones=request.observaciones,
            costo_unitario=request.costo_unitario
        )

        agregado = orden.agregar_material(
            material,
            usuario=usuario
        )

        if agregado is False:
            raise ValueError(
                "No fue posible agregar el material a la orden."
            )

        return material