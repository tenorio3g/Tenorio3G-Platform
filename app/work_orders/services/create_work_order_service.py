from app.assets.repositories.asset_repository import AssetRepository

from app.domains.people.repositories.employee_repository import (
    EmployeeRepository
)

from app.work_orders.domain.work_order import WorkOrder

from app.work_orders.repositories.work_order_repository import (
    WorkOrderRepository
)

from app.work_orders.dto.create_work_order_request import (
    CreateWorkOrderRequest
)

class CreateWorkOrderService:

    def __init__(
        self,
        asset_repository=None,
        employee_repository=None,
        work_order_repository=None
    ):
        self.asset_repository = (
            asset_repository or AssetRepository()
        )

        self.employee_repository = (
            employee_repository or EmployeeRepository()
        )

        self.work_order_repository = (
            work_order_repository or WorkOrderRepository()
        )

    def ejecutar(self, request):
        if not isinstance(request, CreateWorkOrderRequest):
            raise TypeError(
                "Se esperaba un objeto CreateWorkOrderRequest."
            )

        if request.numero is None or not str(request.numero).strip():
            raise ValueError(
                "El número de la orden es obligatorio."
            )

        if request.titulo is None or not str(request.titulo).strip():
            raise ValueError(
                "El título de la orden es obligatorio."
            )

        numero = str(request.numero).strip()
        titulo = str(request.titulo).strip()

        if self.work_order_repository.existe(numero):
            raise ValueError(
                f"Ya existe una orden con el número '{numero}'."
            )

        activo = self.asset_repository.obtener_por_codigo(
            request.codigo_activo
        )

        if activo is None:
            raise ValueError(
                f"No existe el activo '{request.codigo_activo}'."
            )

        solicitante = (
            self.employee_repository.obtener_por_numero(
            request.numero_solicitante
            )
        )

        if solicitante is None:
            raise ValueError(
                "No se encontró al solicitante "
                f"'{request.numero_solicitante}'."
            )

        if not solicitante.esta_activo():
            raise ValueError(
                "El solicitante está inactivo."
            )

        supervisor = (
            self.employee_repository.obtener_por_numero(
                request.numero_supervisor
            )
        )

        if supervisor is None:
            raise ValueError(
                "No se encontró al supervisor "
                f"'{request.numero_supervisor}'."
            )

        if not supervisor.esta_activo():
            raise ValueError(
                "El supervisor está inactivo."
            )

        orden = WorkOrder(
            numero=numero,
            titulo=titulo,
            descripcion=request.descripcion,
            tipo=request.tipo,
            prioridad=request.prioridad,
            solicitante=solicitante,
            supervisor=supervisor,
            activo=activo
        )

        guardada = self.work_order_repository.guardar(
            orden
        )

        if not guardada:
            raise ValueError(
                "No fue posible guardar la orden."
            )

        return orden