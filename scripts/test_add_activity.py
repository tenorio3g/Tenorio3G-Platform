from app.work_orders.dto.add_activity_request import (
    AddActivityRequest
)

from app.work_orders.repositories.work_order_repository import (
    WorkOrderRepository
)

from app.work_orders.services.add_activity_service import (
    AddActivityService
)


repository = WorkOrderRepository()

orden = repository.obtener_por_numero("69926")

service = AddActivityService(
    work_order_repository=repository
)

print("ACTIVIDADES ANTES")
print("-----------------")

for actividad in orden.actividades:
    print("-", actividad.titulo)

request = AddActivityRequest(
    numero_orden="69926",
    titulo="Verificar torque de conexiones",
    descripcion=(
        "Revisar y documentar el torque de las "
        "conexiones eléctricas del tablero."
    ),
    numero_responsable="0003",
    usuario="Fortunato Tenorio"
)

actividad = service.ejecutar(request)

print()
print("ACTIVIDAD AGREGADA")
print("------------------")
print("Título:", actividad.titulo)
print("Responsable:", actividad.responsable.nombre)
print("Estado:", actividad.estado)

print()
print("ACTIVIDADES DESPUÉS")
print("-------------------")

for item in orden.actividades:
    print(
        "-",
        item.titulo,
        "|",
        item.responsable.nombre
    )

print()
print("ÚLTIMO EVENTO DEL TIMELINE")
print("--------------------------")

ultimo_evento = orden.eventos_timeline()[0]

print("Categoría:", ultimo_evento.categoria)
print("Título:", ultimo_evento.titulo)
print("Descripción:", ultimo_evento.descripcion)
print("Usuario:", ultimo_evento.usuario)