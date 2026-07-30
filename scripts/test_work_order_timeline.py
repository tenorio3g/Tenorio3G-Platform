from app.assets.repositories.asset_repository import AssetRepository
from app.domains.people.repositories.employee_repository import (
    EmployeeRepository
)
from app.work_orders.domain.work_order import WorkOrder
from app.work_orders.domain.work_order_activity import WorkOrderActivity
from app.work_orders.domain.work_order_material import WorkOrderMaterial


asset_repository = AssetRepository()
employee_repository = EmployeeRepository()

activo = asset_repository.obtener_por_codigo("ES09")
supervisor = employee_repository.obtener_por_numero("0001")
tecnico = employee_repository.obtener_por_numero("0002")
solicitante = employee_repository.obtener_por_numero("0004")

orden = WorkOrder(
    numero="70100",
    titulo="Prueba Foundation Timeline",
    descripcion="Validar integración de WorkOrder con Timeline.",
    tipo="Prueba",
    prioridad="Alta",
    solicitante=solicitante,
    supervisor=supervisor,
    activo=activo
)

orden.agregar_tecnico(
    tecnico,
    usuario=supervisor.nombre
)

orden.agregar_actividad(
    WorkOrderActivity(
        titulo="Preparar área",
        responsable=tecnico
    ),
    usuario=supervisor.nombre
)

orden.agregar_material(
    WorkOrderMaterial(
        nombre="Cable THHN #12",
        cantidad=15,
        unidad="m"
    ),
    usuario=tecnico.nombre
)

print("Eventos antiguos:", len(orden.eventos))
print("Eventos Timeline:", orden.cantidad_eventos_timeline())

print("\nTIMELINE DE LA ORDEN")

for evento in orden.eventos_timeline():
    print(
        evento.icono,
        evento.categoria,
        "-",
        evento.titulo,
        "-",
        evento.usuario,
        "-",
        evento.descripcion or "",
        "-",
        evento.referencia
    )