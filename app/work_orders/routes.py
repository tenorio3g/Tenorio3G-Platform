from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from . import work_orders

from app.work_orders.dto.create_work_order_request import CreateWorkOrderRequest
from app.work_orders.dto.assign_technician_request import AssignTechnicianRequest
from app.work_orders.dto.add_activity_request import AddActivityRequest
from app.work_orders.dto.add_material_request import AddMaterialRequest

from app.work_orders.repositories.work_order_repository import WorkOrderRepository

from app.work_orders.services.create_work_order_service import CreateWorkOrderService
from app.work_orders.services.assign_technician_service import AssignTechnicianService
from app.work_orders.services.add_activity_service import AddActivityService
from app.work_orders.services.add_material_service import AddMaterialService


# =====================================================
# Repositorios
# =====================================================

work_order_repository = WorkOrderRepository()


# =====================================================
# Servicios
# =====================================================

create_work_order_service = CreateWorkOrderService(
    work_order_repository=work_order_repository
)

assign_technician_service = AssignTechnicianService(
    work_order_repository=work_order_repository
)

add_activity_service = AddActivityService(
    work_order_repository=work_order_repository
)

add_material_service = AddMaterialService(
    work_order_repository=work_order_repository
)

# =====================================================
# Crear Orden
# =====================================================

@work_orders.route("/ordenes/nueva", methods=["GET", "POST"])
def nueva_orden():

    if request.method == "GET":
        return render_template("pages/work_order_create.html")

    create_request = CreateWorkOrderRequest(
        numero=request.form.get("numero"),
        titulo=request.form.get("titulo"),
        descripcion=request.form.get("descripcion"),
        tipo=request.form.get("tipo"),
        prioridad=request.form.get("prioridad"),
        codigo_activo=request.form.get("codigo_activo"),
        numero_solicitante=request.form.get("numero_solicitante"),
        numero_supervisor=request.form.get("numero_supervisor")
    )

    try:
        orden = create_work_order_service.ejecutar(create_request)
        return redirect(url_for("work_orders.detalle", numero=orden.numero))

    except (ValueError, TypeError) as error:
        return render_template(
            "pages/work_order_create.html",
            error=str(error),
            datos=request.form
        )


# =====================================================
# Detalle Orden
# =====================================================

@work_orders.route("/ordenes/<numero>")
def detalle(numero):

    orden = work_order_repository.obtener_por_numero(numero)

    if orden is None:
        return "Orden no encontrada", 404

    return render_template(
        "pages/work_order_detail.html",
        orden=orden
    )


# =====================================================
# Asignar Técnico
# =====================================================

@work_orders.route("/ordenes/<numero>/asignar-tecnico", methods=["GET", "POST"])
def asignar_tecnico(numero):

    orden = work_order_repository.obtener_por_numero(numero)

    if orden is None:
        return "Orden no encontrada", 404

    if request.method == "GET":
        return render_template(
            "pages/assign_technician.html",
            orden=orden
        )

    request_dto = AssignTechnicianRequest(
        numero_orden=numero,
        numero_tecnico=request.form.get("numero_tecnico"),
        usuario="Fortunato Tenorio" # TODO: Replace with dynamic current_user
    )

    try:
        assign_technician_service.ejecutar(request_dto)
        return redirect(url_for("work_orders.detalle", numero=numero))

    except (ValueError, TypeError) as error:
        return render_template(
            "pages/assign_technician.html",
            orden=orden,
            error=str(error),
            numero_tecnico=request.form.get("numero_tecnico", "")
        )


# =====================================================
# Agregar Actividad
# =====================================================

@work_orders.route("/ordenes/<numero>/agregar-actividad", methods=["GET", "POST"])
def agregar_actividad(numero):

    orden = work_order_repository.obtener_por_numero(numero)

    if orden is None:
        return "Orden no encontrada", 404

    if request.method == "GET":
        return render_template(
            "pages/add_activity.html",
            orden=orden
        )

    request_dto = AddActivityRequest(
        numero_orden=numero,
        titulo=request.form.get("titulo"),
        descripcion=request.form.get("descripcion"),
        numero_responsable=request.form.get("numero_responsable"),
        usuario="Fortunato Tenorio" # TODO: Replace with dynamic current_user
    )

    try:
        add_activity_service.ejecutar(request_dto)
        return redirect(url_for("work_orders.detalle", numero=numero))

    except (ValueError, TypeError) as error:
        return render_template(
            "pages/add_activity.html",
            orden=orden,
            error=str(error),
            datos=request.form
        )
    


    # =====================================================
# Agregar Material
# =====================================================

@work_orders.route(
    "/ordenes/<numero>/agregar-material",
    methods=["GET", "POST"]
)
def agregar_material(numero):

    orden = work_order_repository.obtener_por_numero(numero)

    if orden is None:
        return "Orden no encontrada", 404

    if request.method == "GET":
        return render_template(
            "pages/add_material.html",
            orden=orden
        )

    request_dto = AddMaterialRequest(
        numero_orden=numero,
        nombre=request.form.get("nombre"),
        cantidad=request.form.get("cantidad"),
        unidad=request.form.get("unidad"),
        usuario="Fortunato Tenorio",
        codigo=request.form.get("codigo"),
        marca=request.form.get("marca"),
        descripcion=request.form.get("descripcion"),
        observaciones=request.form.get("observaciones"),
        costo_unitario=request.form.get("costo_unitario")
    )

    try:
        add_material_service.ejecutar(request_dto)

        return redirect(
            url_for(
                "work_orders.detalle",
                numero=numero
            )
        )

    except (ValueError, TypeError) as error:
        return render_template(
            "pages/add_material.html",
            orden=orden,
            error=str(error),
            datos=request.form
        )