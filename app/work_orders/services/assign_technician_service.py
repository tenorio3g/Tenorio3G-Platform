from app.work_orders.dto.assign_technician_request import (
    AssignTechnicianRequest
)

from app.work_orders.repositories.work_order_repository import (
    WorkOrderRepository
)

from app.domains.people.repositories.employee_repository import (
    EmployeeRepository
)


class AssignTechnicianService:

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

        if not isinstance(request, AssignTechnicianRequest):
            raise TypeError(
            "Se esperaba un objeto AssignTechnicianRequest."
        )

        numero_orden = str(request.numero_orden).strip()
        numero_tecnico = str(request.numero_tecnico).strip()
        usuario = str(request.usuario).strip()

        if not numero_orden:
            raise ValueError(
            "El número de la orden es obligatorio."
        )

        if not numero_tecnico:
            raise ValueError(
            "Debe indicar el número del técnico."
        )

        if not usuario:
            raise ValueError(
            "El usuario que realiza la asignación es obligatorio."
        )

        orden = self.work_order_repository.obtener_por_numero(
            numero_orden
        )

        if orden is None:
            raise ValueError(
            f"No existe la orden '{numero_orden}'."
        )

        tecnico = self.employee_repository.obtener_por_numero(
            numero_tecnico
        )

        if tecnico is None:
            raise ValueError(
            f"No existe el empleado '{numero_tecnico}'."
        )

        if not tecnico.esta_activo():
            raise ValueError(
            "El empleado seleccionado está inactivo."
        )

        agregado = orden.agregar_tecnico(
            tecnico,
            usuario=usuario
        )

        if not agregado:
            raise ValueError(
                f"{tecnico.nombre} ya está asignado a esta orden."
        )

        return orden