from app.work_orders.dto.create_work_order_request import (
    CreateWorkOrderRequest
)

from app.work_orders.repositories.work_order_repository import (
    WorkOrderRepository
)

from app.work_orders.services.create_work_order_service import (
    CreateWorkOrderService
)


# =====================================
# Preparar repositorio y servicio
# =====================================

repository = WorkOrderRepository()

service = CreateWorkOrderService(
    work_order_repository=repository
)


# =====================================
# Crear solicitud
# =====================================

request = CreateWorkOrderRequest(
    numero="70150",
    titulo="Instalación de servicio eléctrico",
    descripcion=(
        "Instalar alimentación eléctrica para "
        "un nuevo equipo de producción."
    ),
    tipo="Proyecto",
    prioridad="Alta",
    codigo_activo="ES09",
    numero_solicitante="0004",
    numero_supervisor="0001"
)


# =====================================
# Crear y comprobar la orden
# =====================================

try:
    orden = service.ejecutar(request)

    print("ORDEN CREADA CORRECTAMENTE")
    print("--------------------------")
    print("ID interno:", orden.id)
    print("Número:", orden.numero)
    print("Título:", orden.titulo)
    print("Descripción:", orden.descripcion)
    print("Tipo:", orden.tipo)
    print("Prioridad:", orden.prioridad)
    print("Estado:", orden.estado)
    print("Activo:", orden.activo.nombre)
    print("Solicitante:", orden.solicitante.nombre)
    print("Supervisor:", orden.supervisor.nombre)

    # =====================================
    # Recuperar la orden del repositorio
    # =====================================

    orden_guardada = repository.obtener_por_numero("70150")

    print()
    print("VERIFICACIÓN DEL REPOSITORIO")
    print("----------------------------")
    print("¿Existe?:", repository.existe("70150"))
    print(
        "Orden recuperada:",
        (
            orden_guardada.titulo
            if orden_guardada
            else "No encontrada"
        )
    )

    # =====================================
    # Comprobar que no permita duplicados
    # =====================================

    print()
    print("PRUEBA DE ORDEN DUPLICADA")
    print("-------------------------")

    request_duplicado = CreateWorkOrderRequest(
        numero="70150",
        titulo="Orden duplicada",
        descripcion="Esta orden no debe guardarse.",
        tipo="Prueba",
        prioridad="Baja",
        codigo_activo="ES09",
        numero_solicitante="0004",
        numero_supervisor="0001"
    )

    try:
        service.ejecutar(request_duplicado)

        print(
            "ERROR: el sistema permitió duplicar "
            "el número de orden."
        )

    except ValueError as error:
        print("Duplicado rechazado correctamente.")
        print("Motivo:", error)

except (ValueError, TypeError) as error:
    print("NO SE PUDO CREAR LA ORDEN")
    print("-------------------------")
    print("Motivo:", error)