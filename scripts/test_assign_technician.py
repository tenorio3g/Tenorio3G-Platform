from app.work_orders.repositories.work_order_repository import (
    WorkOrderRepository
)

from app.work_orders.services.assign_technician_service import (
    AssignTechnicianService
)

from app.work_orders.dto.assign_technician_request import (
    AssignTechnicianRequest
)


# =====================================
# Preparar repositorio
# =====================================

repository = WorkOrderRepository()

orden = repository.obtener_por_numero("69926")

print("ORDEN")
print(orden.numero)
print()

print("TÉCNICOS ANTES")
for tecnico in orden.tecnicos:
    print("-", tecnico.nombre)

print()


# =====================================
# Crear servicio
# =====================================

service = AssignTechnicianService(
    work_order_repository=repository
)


request = AssignTechnicianRequest(
    numero_orden="69926",
    numero_tecnico="0003",
    usuario="Fortunato Tenorio"
)


service.ejecutar(request)

print("TÉCNICOS DESPUÉS")

for tecnico in orden.tecnicos:
    print("-", tecnico.nombre)

print()

print("TIMELINE")

for evento in orden.timeline:
    print(
        evento.icono,
        evento.titulo,
        "-",
        evento.usuario
    )