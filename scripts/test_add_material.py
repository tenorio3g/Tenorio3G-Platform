from app.work_orders.dto.add_material_request import (
    AddMaterialRequest
)

from app.work_orders.repositories.work_order_repository import (
    WorkOrderRepository
)

from app.work_orders.services.add_material_service import (
    AddMaterialService
)


repository = WorkOrderRepository()

orden = repository.obtener_por_numero("69926")

if orden is None:
    raise ValueError(
        "No se encontró la orden 69926 para realizar la prueba."
    )

service = AddMaterialService(
    work_order_repository=repository
)

print("MATERIALES ANTES")
print("----------------")

for material in orden.materiales:
    print(
        "-",
        material.nombre,
        material.cantidad,
        material.unidad
    )

request = AddMaterialRequest(
    numero_orden="69926",
    nombre="Cable THHN calibre 12",
    cantidad=20,
    unidad="metros",
    codigo="MAT-001",
    marca="Condumex",
    descripcion="Cable de cobre color verde",
    observaciones=(
        "Utilizado para alimentación del tablero ES09."
    ),
    costo_unitario=24.50,
    usuario="Fortunato Tenorio"
)

material = service.ejecutar(request)

print()
print("MATERIAL AGREGADO")
print("-----------------")
print("Nombre:", material.nombre)
print("Código:", material.codigo)
print("Marca:", material.marca)
print("Cantidad:", material.cantidad)
print("Unidad:", material.unidad)
print("Costo unitario:", material.costo_unitario)
print("Costo total:", material.costo_total)

print()
print("MATERIALES DESPUÉS")
print("------------------")

for item in orden.materiales:
    print(
        "-",
        item.nombre,
        "|",
        item.cantidad,
        item.unidad,
        "| Costo total:",
        item.costo_total
    )

print()
print("ÚLTIMO EVENTO DEL TIMELINE")
print("--------------------------")

eventos = orden.eventos_timeline()

if eventos:
    ultimo_evento = eventos[0]

    print("Categoría:", ultimo_evento.categoria)
    print("Título:", ultimo_evento.titulo)
    print("Descripción:", ultimo_evento.descripcion)
    print("Usuario:", ultimo_evento.usuario)
else:
    print("No se encontraron eventos en el Timeline.")

print()
print("COSTOS DE LA ORDEN")
print("------------------")
print("Costo de materiales:", orden.costo_materiales)
print("Costo total:", orden.costo_total)