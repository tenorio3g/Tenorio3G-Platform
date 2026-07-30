from app.assets.repositories.asset_repository import AssetRepository
from app.work_orders.domain.work_order import WorkOrder
from app.work_orders.domain.work_order_activity import WorkOrderActivity


asset_repository = AssetRepository()
activo = asset_repository.obtener_por_codigo("ES09")

orden = WorkOrder(
    numero="70001",
    titulo="Prueba del ciclo de vida",
    descripcion="Validación de estados de una Orden de Trabajo.",
    tipo="Prueba",
    prioridad="Normal",
    solicitante="Ingeniería",
    supervisor="Fortunato",
    activo=activo
)

actividad_1 = WorkOrderActivity(
    titulo="Preparar área",
    responsable="Fortunato"
)

actividad_2 = WorkOrderActivity(
    titulo="Realizar trabajo",
    responsable="Fortunato"
)

orden.agregar_actividad(actividad_1)
orden.agregar_actividad(actividad_2)

print("Estado inicial:", orden.estado)

resultado = orden.iniciar(usuario="Fortunato")
print("Intentar iniciar sin asignar:", resultado)
print("Estado:", orden.estado)

resultado = orden.asignar(usuario="Fortunato")
print("Asignar orden:", resultado)
print("Estado:", orden.estado)

resultado = orden.iniciar(usuario="Fortunato")
print("Iniciar orden:", resultado)
print("Estado:", orden.estado)

resultado = orden.finalizar(usuario="Fortunato")
print("Finalizar con actividades pendientes:", resultado)
print("Avance:", orden.porcentaje_avance(), "%")
print("Estado:", orden.estado)

actividad_1.finalizar()
actividad_2.finalizar()

print("Avance después de finalizar actividades:", orden.porcentaje_avance(), "%")

resultado = orden.finalizar(usuario="Fortunato")
print("Finalizar orden:", resultado)
print("Estado:", orden.estado)

resultado = orden.cerrar(usuario="Fortunato")
print("Cerrar orden:", resultado)
print("Estado final:", orden.estado)

print("\nHISTORIAL DE ESTADOS")

for registro in orden.historial:
    print(
        registro.fecha.strftime("%d/%m/%Y %H:%M:%S"),
        "-",
        registro.estado_anterior,
        "→",
        registro.estado_nuevo,
        "- Usuario:",
        registro.usuario
    )