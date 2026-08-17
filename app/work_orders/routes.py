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

from app.domains.work_orders.bootstrap import (
    assign_work_order,
    cancel_work_order,
    close_work_order,
    complete_work_order,
    get_work_order_detail,
    hold_work_order,
    resume_work_order,
    start_work_order,
)

from app.domains.work_orders.presentation import (
    WorkOrderDetailPresenter,
)

from app.domains.work_orders.use_cases import (
    AssignWorkOrderCommand,
    CancelWorkOrderCommand,
    CloseWorkOrderCommand,
    CompleteWorkOrderCommand,
    GetWorkOrderDetailQuery,
    HoldWorkOrderCommand,
    ResumeWorkOrderCommand,
    StartWorkOrderCommand,
)

from app.domains.work_orders.technicians.bootstrap import (
    list_work_order_technicians,
    assign_technician_to_work_order,
    unassign_technician_from_work_order,
)

from app.domains.work_orders.technicians.use_cases import (
    ListWorkOrderTechniciansQuery,
    AssignTechnicianToWorkOrderCommand,
    UnassignTechnicianFromWorkOrderCommand,
)

from app.domains.work_orders.technicians.presentation import (
    WorkOrderTechniciansPresenter,
)
from datetime import datetime
from app.domains.work_orders.activities.bootstrap import (
    list_work_order_activities,
    create_work_order_activity,
    complete_work_order_activity,
    start_work_order_activity,
)

from app.domains.work_orders.activities.presentation import (
    WorkOrderActivitiesPresenter,
)

from app.domains.work_orders.activities.use_cases import (
    ListWorkOrderActivitiesQuery,
    CreateWorkOrderActivityCommand,
    CompleteWorkOrderActivityCommand,
    StartWorkOrderActivityCommand,
)



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

    try:
        result = get_work_order_detail.execute(
            GetWorkOrderDetailQuery(
                code=numero,
            )
        )

    except ValueError:
        return (
            "Orden no encontrada",
            404,
        )

    orden = WorkOrderDetailPresenter.present(
        result.work_order,
        result.asset,
        result.requester,
        result.supervisor,
    )

    technicians_result = (
        list_work_order_technicians.execute(
            ListWorkOrderTechniciansQuery(
                work_order_code=numero,
            )
        )
    )

    technicians = (
        WorkOrderTechniciansPresenter.present(
            technicians_result
        )
    )

    activities_result = (
        list_work_order_activities.execute(
            ListWorkOrderActivitiesQuery(
                work_order_code=numero
            )
        )
    )

    activities = (
        WorkOrderActivitiesPresenter.present(
            activities_result
        )
    )

    return render_template(
        "pages/work_order_detail_v2.html",
        orden=orden,
        technicians=technicians,
        activities=activities,
    )

# =====================================================
# Asignar Técnico
# =====================================================

@work_orders.route(
    "/ordenes/<numero>/asignar-tecnico",
    methods=["GET", "POST"],
)
def asignar_tecnico(
    numero: str,
):

    try:
        detail_result = (
            get_work_order_detail.execute(
                GetWorkOrderDetailQuery(
                    code=numero,
                )
            )
        )

    except ValueError:
        return (
            "Orden no encontrada",
            404,
        )

    orden = WorkOrderDetailPresenter.present(
        detail_result.work_order,
        detail_result.asset,
        detail_result.requester,
        detail_result.supervisor,
    )

    if request.method == "GET":
        return render_template(
            "pages/assign_technician_v2.html",
            orden=orden,
        )

    person_code = request.form.get(
        "person_code",
        "",
    )

    try:
        assign_technician_to_work_order.execute(
            AssignTechnicianToWorkOrderCommand(
                work_order_code=numero,
                person_code=person_code,
                assigned_at=datetime.now(),
            )
        )

    except ValueError as exc:
        return render_template(
            "pages/assign_technician_v2.html",
            orden=orden,
            error=str(exc),
            person_code=person_code,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
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

@work_orders.post(
    "/ordenes/<numero>/asignar"
)
def assign_work_order_route(
    numero: str,
):

    try:
        assign_work_order.execute(
            AssignWorkOrderCommand(
                code=numero,
            )
        )

    except ValueError as exc:
        return (
            str(exc),
            400,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )


@work_orders.post(
    "/ordenes/<numero>/iniciar"
)
def start_work_order_route(
    numero: str,
):

    try:
        start_work_order.execute(
            StartWorkOrderCommand(
                code=numero,
            )
        )

    except ValueError as exc:
        return (
            str(exc),
            400,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )

@work_orders.post(
    "/ordenes/<numero>/pausar"
)
def hold_work_order_route(
    numero: str,
):

    try:
        hold_work_order.execute(
            HoldWorkOrderCommand(
                code=numero,
            )
        )

    except ValueError as exc:
        return (
            str(exc),
            400,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )


@work_orders.post(
    "/ordenes/<numero>/reanudar"
)
def resume_work_order_route(
    numero: str,
):

    try:
        resume_work_order.execute(
            ResumeWorkOrderCommand(
                code=numero,
            )
        )

    except ValueError as exc:
        return (
            str(exc),
            400,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )


@work_orders.post(
    "/ordenes/<numero>/completar"
)
def complete_work_order_route(
    numero: str,
):

    try:
        complete_work_order.execute(
            CompleteWorkOrderCommand(
                code=numero,
            )
        )

    except ValueError as exc:
        return (
            str(exc),
            400,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )


@work_orders.post(
    "/ordenes/<numero>/cerrar"
)
def close_work_order_route(
    numero: str,
):

    try:
        close_work_order.execute(
            CloseWorkOrderCommand(
                code=numero,
            )
        )

    except ValueError as exc:
        return (
            str(exc),
            400,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )


@work_orders.post(
    "/ordenes/<numero>/cancelar"
)
def cancel_work_order_route(
    numero: str,
):

    try:
        cancel_work_order.execute(
            CancelWorkOrderCommand(
                code=numero,
            )
        )

    except ValueError as exc:
        return (
            str(exc),
            400,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )

@work_orders.post(
    "/ordenes/<numero>/tecnicos/<person_code>/quitar"
)
def unassign_technician_route(
    numero: str,
    person_code: str,
):

    try:
        unassign_technician_from_work_order.execute(
            UnassignTechnicianFromWorkOrderCommand(
                work_order_code=numero,
                person_code=person_code,
            )
        )

    except ValueError as exc:
        return (
            str(exc),
            400,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )

@work_orders.route(
    "/ordenes/<numero>/actividades/nueva",
    methods=["GET", "POST"],
)
def create_work_order_activity_route(
    numero: str,
):

    try:
        detail_result = (
            get_work_order_detail.execute(
                GetWorkOrderDetailQuery(
                    code=numero,
                )
            )
        )

    except ValueError:
        return (
            "Orden no encontrada",
            404,
        )

    orden = WorkOrderDetailPresenter.present(
        detail_result.work_order,
        detail_result.asset,
        detail_result.requester,
        detail_result.supervisor,
    )

    if request.method == "GET":
        return render_template(
            "pages/create_work_order_activity_v2.html",
            orden=orden,
        )

    estimated_minutes_raw = (
        request.form.get(
            "estimated_minutes",
            "",
        )
        .strip()
    )

    estimated_minutes = (
        int(estimated_minutes_raw)
        if estimated_minutes_raw
        else None
    )

    try:
        create_work_order_activity.execute(
            CreateWorkOrderActivityCommand(
                code=request.form.get(
                    "code",
                    "",
                ),
                work_order_code=numero,
                title=request.form.get(
                    "title",
                    "",
                ),
                responsible_person_code=(
                    request.form.get(
                        "responsible_person_code",
                        "",
                    )
                ),
                description=request.form.get(
                    "description",
                    "",
                ),
                estimated_minutes=(
                    estimated_minutes
                ),
            )
        )

    except (ValueError, TypeError) as exc:
        return render_template(
            "pages/create_work_order_activity_v2.html",
            orden=orden,
            error=str(exc),
            data=request.form,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )


@work_orders.post(
    "/ordenes/<numero>/actividades/<activity_code>/iniciar"
)
def start_work_order_activity_route(
    numero: str,
    activity_code: str,
):

    try:
        start_work_order_activity.execute(
            StartWorkOrderActivityCommand(
                code=activity_code,
                started_at=datetime.now(),
            )
        )

    except ValueError as exc:
        return (
            str(exc),
            400,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )


@work_orders.post(
    "/ordenes/<numero>/actividades/<activity_code>/finalizar"
)
def complete_work_order_activity_route(
    numero: str,
    activity_code: str,
):

    try:
        complete_work_order_activity.execute(
            CompleteWorkOrderActivityCommand(
                code=activity_code,
                completed_at=datetime.now(),
            )
        )

    except ValueError as exc:
        return (
            str(exc),
            400,
        )

    return redirect(
        url_for(
            "work_orders.detalle",
            numero=numero,
        )
    )