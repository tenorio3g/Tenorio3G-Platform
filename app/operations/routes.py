from datetime import date, datetime, timedelta

from flask import (
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from . import operations
from app.domains.identity.authentication import login_required
from app.operations.daily_reports.bootstrap import (
    get_daily_operational_report,
)
from app.operations.daily_reports.queries import (
    GetDailyOperationalReportQuery,
)
from app.operations.daily_reports.presenters import (
    DailyReportTextPresenter,
)

from app.operations.operational_activities.bootstrap import (
    complete_operational_activity,
    create_operational_activity,
    operational_activity_repository,
)
from app.domains.work_orders.bootstrap import (
    get_work_order,
    list_work_orders,
)
from app.domains.work_orders.use_cases import (
    GetWorkOrderQuery,
)
from app.operations.services.operations_service import OperationsService


@operations.route("/operaciones")
def index():

    service = OperationsService()

    resumen = service.resumen()
    metricas = service.obtener_metricas()
    ordenes_recientes = service.obtener_ordenes_recientes()
    activos_en_riesgo = service.obtener_activos_en_riesgo()
    tecnicos = service.obtener_tecnicos()

    return render_template(
        "pages/operations_dashboard.html",
        resumen=resumen,
        metricas=metricas,
        ordenes_recientes=ordenes_recientes,
        activos_en_riesgo=activos_en_riesgo,
        tecnicos=tecnicos
    )

@operations.route(
    "/operaciones/actividades/nueva",
    methods=["GET", "POST"],
)
@login_required
def new_operational_activity_route():

    if request.method == "GET":
        work_orders_result = list_work_orders.execute()

        return render_template(
            "pages/create_operational_activity.html",
            work_orders=work_orders_result.work_orders,
        )

    person_code = str(
        session.get(
            "person_code",
            "",
        )
    ).strip().upper()

    if not person_code:
        return (
            "Usuario autenticado sin persona asociada",
            400,
        )

    try:
        started_at_raw = request.form.get(
            "started_at",
            "",
        ).strip()

        started_at = datetime.fromisoformat(
            started_at_raw
        )

        work_order_code = (
            request.form.get(
                "work_order_code",
                "",
            ).strip().upper()
            or None
        )

        if work_order_code:
            try:
                get_work_order.execute(
                    GetWorkOrderQuery(
                        code=work_order_code,
                    )
                )
            except ValueError as exc:
                if str(exc) == "work order not found":
                    raise ValueError(
                        "La orden de trabajo seleccionada "
                        "no existe."
                    ) from exc

                raise

        activity = create_operational_activity.execute(
            description=request.form.get(
                "description",
                "",
            ),
            started_at=started_at,
            area=request.form.get(
                "area",
                "",
            ),
            location_description=request.form.get(
                "location_description",
                "",
            ),
            asset_code=request.form.get(
                "asset_code",
                "",
            )
            or None,
            work_order_code=work_order_code,
            created_by_person_code=person_code,
        )

    except (ValueError, TypeError) as exc:
        work_orders_result = list_work_orders.execute()

        return render_template(
            "pages/create_operational_activity.html",
            error=str(exc),
            data=request.form,
            work_orders=work_orders_result.work_orders,
        )

    return redirect(
        url_for(
            "operations.operational_activity_created_route",
            code=activity.code,
        )
    )



@operations.get(
    "/operaciones/actividades/<code>/registrada"
)
@login_required
def operational_activity_created_route(code):

    normalized_code = str(code).strip().upper()

    return render_template(
        "pages/operational_activity_created.html",
        activity_code=normalized_code,
    )


def format_duration(total_seconds: int) -> str:

    total_minutes = total_seconds // 60

    hours, minutes = divmod(
        total_minutes,
        60,
    )

    if hours and minutes:
        return f"{hours} h {minutes} min"

    if hours:
        return f"{hours} h"

    return f"{minutes} min"


@operations.get(
    "/operaciones/reporte-diario"
)
@login_required
def daily_operational_report_route():

    selected_date = (
        request.args.get("fecha", "").strip()
    )

    if selected_date:
        try:
            report_date = date.fromisoformat(
                selected_date
            )
        except ValueError:
            return (
                "La fecha seleccionada no es valida.",
                400,
            )
    else:
        report_date = current_date()

    query = GetDailyOperationalReportQuery(
        report_date=report_date,
    )

    report = (
        get_daily_operational_report.execute(
            query
        )
    )

    shareable_report = (
        DailyReportTextPresenter.present(
            report
        )
    )

    previous_date = (
        report.report_date
        - timedelta(days=1)
    )

    next_date = (
        report.report_date
        + timedelta(days=1)
    )

    return render_template(
        "pages/daily_operational_report.html",
        report=report,
        effective_time=format_duration(
            report.effective_seconds
        ),
        shareable_report=shareable_report,
        previous_date=previous_date,
        next_date=next_date,
    )


def current_date() -> date:
    return date.today()


def current_datetime() -> datetime:
    return datetime.now()


@operations.get(
    "/operaciones/actividades/hoy"
)
@login_required
def today_operational_activities_route():

    report_date = current_date()

    activities = (
        operational_activity_repository
        .list_by_date(report_date)
    )

    return render_template(
        "pages/today_operational_activities.html",
        report_date=report_date,
        activities=activities,
    )


@operations.route(
    "/operaciones/actividades/<code>/finalizar",
    methods=["GET", "POST"],
)
@login_required
def complete_operational_activity_route(code):

    normalized_code = str(
        code
    ).strip().upper()

    activity = (
        operational_activity_repository
        .get_by_code(normalized_code)
    )

    if activity is None:
        abort(404)

    if activity.status.value == "COMPLETED":
        abort(409)

    if request.method == "POST":

        person_code = str(
            session.get(
                "person_code",
                "",
            )
        ).strip().upper()

        if not person_code:
            return (
                "Usuario autenticado sin persona asociada",
                400,
            )

        ended_at_raw = request.form.get(
            "ended_at",
            "",
        ).strip()

        result_notes = request.form.get(
            "result_notes",
            "",
        )

        try:
            ended_at = datetime.fromisoformat(
                ended_at_raw
            )
        except (ValueError, TypeError):
            return (
                render_template(
                    "pages/complete_operational_activity.html",
                    activity=activity,
                    error="Fecha y hora de termino invalidas",
                    data=request.form,
                ),
                400,
            )

        try:
            complete_operational_activity.execute(
                code=normalized_code,
                ended_at=ended_at,
                result_notes=result_notes,
                completed_at=current_datetime(),
                completed_by_person_code=person_code,
            )
        except ValueError as exc:
            return (
                render_template(
                    "pages/complete_operational_activity.html",
                    activity=activity,
                    error=str(exc),
                    data=request.form,
                ),
                400,
            )

        return redirect(
            url_for(
                "operations.today_operational_activities_route"
            )
        )

    return render_template(
        "pages/complete_operational_activity.html",
        activity=activity,
    )

