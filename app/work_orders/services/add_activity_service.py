from app.domains.people.repositories.employee_repository import (
    EmployeeRepository
)

from app.work_orders.domain.work_order_activity import (
    WorkOrderActivity
)

from app.work_orders.dto.add_activity_request import (
    AddActivityRequest
)

from app.work_orders.repositories.work_order_repository import (
    WorkOrderRepository
)


class AddActivityService:

    def __init__(
        self,
        work_order_repository=None,
        employee_repository=None
    ):
        self.work_order_repository = (
            work_order_repository
            or WorkOrderRepository()
        )

        self.employee_repository = (
            employee_repository
            or EmployeeRepository()
        )

    def ejecutar(self, request):

        if not isinstance(request, AddActivityRequest):
            raise TypeError(
                "Se esperaba un objeto AddActivityRequest."
            )

        numero_orden = str(
            request.numero_orden or ""
        ).strip()

        titulo = str(
            request.titulo or ""
        ).strip()

        descripcion = str(
            request.descripcion or ""
        ).strip()

        numero_responsable = str(
            request.numero_responsable or ""
        ).strip()

        usuario = str(
            request.usuario or ""
        ).strip()

        if not numero_orden:
            raise ValueError(
                "El número de la orden es obligatorio."
            )

        if not titulo:
            raise ValueError(
                "El título de la actividad es obligatorio."
            )

        if not numero_responsable:
            raise ValueError(
                "Debe seleccionar un responsable."
            )

        if not usuario:
            raise ValueError(
                "El usuario que registra la actividad es obligatorio."
            )

        orden = (
            self.work_order_repository
            .obtener_por_numero(numero_orden)
        )

        if orden is None:
            raise ValueError(
                f"No existe la orden '{numero_orden}'."
            )

        responsable = (
            self.employee_repository
            .obtener_por_numero(numero_responsable)
        )

        if responsable is None:
            raise ValueError(
                f"No existe el empleado '{numero_responsable}'."
            )

        if not responsable.esta_activo():
            raise ValueError(
                "El responsable seleccionado está inactivo."
            )

        actividad = WorkOrderActivity(
            titulo=titulo,
            descripcion=descripcion,
            responsable=responsable
        )

        agregada = orden.agregar_actividad(
            actividad,
            usuario=usuario
        )

        if not agregada:
            raise ValueError(
                "No fue posible agregar la actividad."
            )

        return actividad