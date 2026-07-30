from app.domains.people.domain.employee import Employee
from app.domains.people.domain.employee_role import EmployeeRole

from app.assets.repositories.asset_repository import AssetRepository

from app.work_orders.domain.work_order import WorkOrder


asset_repository = AssetRepository()

activo = asset_repository.obtener_por_codigo("ES09")

fortu = Employee(
    numero_empleado="0001",
    nombre="Fortunato Tenorio",
    rol=EmployeeRole.SUPERVISOR
)

orden = WorkOrder(
    numero="70050",
    titulo="Prueba Employee",
    descripcion="Validar integración.",
    tipo="Prueba",
    prioridad="Alta",
    solicitante=fortu,
    supervisor=fortu,
    activo=activo
)

print(orden.supervisor.nombre)
print(orden.supervisor.rol)
print(orden.solicitante.nombre)