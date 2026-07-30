import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from app.work_orders.domain.work_order import WorkOrder
from app.work_orders.domain.work_order_material import WorkOrderMaterial
from app.work_orders.domain.work_order_tool import WorkOrderTool


orden = WorkOrder(
    numero="69926",
    titulo="Instalación de circuito para TV",
    descripcion="Agregar alimentación eléctrica para TV en línea.",
    tipo="Proyecto",
    prioridad="Alta",
    solicitante="Ingeniería",
    supervisor="Fortunato",
    activo="ES09"
)

orden.agregar_tecnico("Fortunato")

orden.agregar_material(
    WorkOrderMaterial(
        nombre="Cable THHN #12",
        cantidad=20,
        unidad="m"
    )
)

orden.agregar_herramienta(
    WorkOrderTool(
        nombre="Rotomartillo"
    )
)

orden.iniciar()

print("ORDEN:", orden.numero)
print("TÍTULO:", orden.titulo)
print("ESTADO:", orden.estado)
print("TÉCNICOS:", orden.cantidad_tecnicos())
print("MATERIAL:", orden.materiales[0].nombre, orden.materiales[0].cantidad, orden.materiales[0].unidad)
print("HERRAMIENTA:", orden.herramientas[0].nombre)