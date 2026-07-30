from app.assets.repositories.asset_repository import AssetRepository

from app.domains.people.repositories.employee_repository import (
    EmployeeRepository
)

from app.work_orders.domain.work_order import WorkOrder
from app.work_orders.domain.work_order_activity import WorkOrderActivity
from app.work_orders.domain.work_order_material import WorkOrderMaterial
from app.work_orders.domain.work_order_tool import WorkOrderTool


class WorkOrderRepository:

    def __init__(self):
        self.ordenes = {}

    # =====================================
    # Persistencia en memoria
    # =====================================

    def guardar(self, orden):
        if orden is None:
            return False

        self.ordenes[str(orden.numero)] = orden
        return True

    def existe(self, numero):
        return str(numero) in self.ordenes

    def obtener_todas(self):
        return list(self.ordenes.values())

    # =====================================
    # Consultas
    # =====================================

    def obtener_por_numero(self, numero):
        numero = str(numero)

        if numero in self.ordenes:
            return self.ordenes[numero]

        if numero == "69926":
            orden = self._crear_orden_demostracion()

            # La guardamos para que la siguiente consulta
            # recupere la misma instancia.
            self.guardar(orden)

            return orden

        return None

    # =====================================
    # Datos de demostración
    # =====================================

    def _crear_orden_demostracion(self):
        asset_repository = AssetRepository()
        employee_repository = EmployeeRepository()

        activo = asset_repository.obtener_por_codigo("ES09")

        supervisor = employee_repository.obtener_por_numero("0001")
        tecnico = employee_repository.obtener_por_numero("0002")
        solicitante = employee_repository.obtener_por_numero("0004")

        orden = WorkOrder(
            numero="69926",
            titulo="Instalación de circuito para TV",
            descripcion=(
                "Agregar alimentación eléctrica para TV en línea."
            ),
            tipo="Proyecto",
            prioridad="Alta",
            solicitante=solicitante,
            supervisor=supervisor,
            activo=activo
        )

        orden.agregar_tecnico(
            tecnico,
            usuario=supervisor.nombre
        )

        orden.agregar_material(
            WorkOrderMaterial(
                nombre="Cable THHN #12",
                cantidad=20,
                unidad="m"
            ),
            usuario=tecnico.nombre
        )

        orden.agregar_herramienta(
            WorkOrderTool(
                nombre="Rotomartillo"
            )
        )

        orden.agregar_actividad(
            WorkOrderActivity(
                titulo="Preparar área de trabajo",
                descripcion=(
                    "Revisar condiciones del área "
                    "y preparar herramientas."
                ),
                responsable=tecnico
            ),
            usuario=supervisor.nombre
        )

        actividad_2 = WorkOrderActivity(
            titulo="Instalar tubería EMT",
            descripcion=(
                "Instalación de tubería para "
                "canalización del circuito."
            ),
            responsable=tecnico
        )

        actividad_2.finalizar()

        orden.agregar_actividad(
            actividad_2,
            usuario=supervisor.nombre
        )

        orden.agregar_actividad(
            WorkOrderActivity(
                titulo="Cablear circuito",
                descripcion=(
                    "Cableado del circuito hacia "
                    "el punto de instalación."
                ),
                responsable=tecnico
            ),
            usuario=supervisor.nombre
        )

        return orden