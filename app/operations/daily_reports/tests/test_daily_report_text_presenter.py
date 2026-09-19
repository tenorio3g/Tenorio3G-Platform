from datetime import date, datetime
from types import SimpleNamespace


def test_should_format_operational_activities_for_sharing():

    from app.operations.daily_reports.presenters import (
        DailyReportTextPresenter,
    )

    report = SimpleNamespace(
        report_date=date(
            2026,
            9,
            18,
        ),
        work_orders=[],
        operational_activities=[
            SimpleNamespace(
                code="OPA-001",
                description=(
                    "Revision de alumbrado exterior"
                ),
                started_at=datetime(
                    2026,
                    9,
                    18,
                    7,
                    0,
                ),
                ended_at=datetime(
                    2026,
                    9,
                    18,
                    9,
                    0,
                ),
                result_notes=(
                    "Alumbrado revisado correctamente"
                ),
                area="EXTERIOR",
                location_description="",
                asset_code=None,
                work_order_code=None,
                status="COMPLETED",
            ),
            SimpleNamespace(
                code="OPA-002",
                description=(
                    "Revision de alimentacion de camaras"
                ),
                started_at=datetime(
                    2026,
                    9,
                    18,
                    11,
                    30,
                ),
                ended_at=None,
                result_notes="",
                area="SISTEMAS",
                location_description="MD2",
                asset_code=None,
                work_order_code=None,
                status="IN_PROGRESS",
            ),
        ],
    )

    text = DailyReportTextPresenter.present(
        report
    )

    assert "*REPORTE DE ACTIVIDADES*" in text
    assert "*18/09/2026*" in text

    assert "*07:00 - 09:00*" in text
    assert (
        "Revision de alumbrado exterior"
        in text
    )
    assert (
        "*Resultado:* Alumbrado revisado correctamente"
        in text
    )

    assert "*11:30 - En proceso*" in text
    assert (
        "Revision de alimentacion de camaras"
        in text
    )

    assert "*Area:* SISTEMAS" in text
    assert "*Ubicacion:* MD2" in text

    assert "OPA-001" not in text
    assert "OPA-002" not in text


def test_should_format_work_order_activities_for_sharing():

    from app.operations.daily_reports.presenters import (
        DailyReportTextPresenter,
    )

    report = SimpleNamespace(
        report_date=date(
            2026,
            9,
            18,
        ),
        work_orders=[
            SimpleNamespace(
                work_order_code="WO-70000",
                title=(
                    "Mantenimiento de alumbrado MD1"
                ),
                asset_code="ALUM-MD1",
                activities=[
                    SimpleNamespace(
                        activity_code=(
                            "WO-70000-ACT-001"
                        ),
                        title=(
                            "Reemplazo de barras LED"
                        ),
                        status="COMPLETED",
                        completion_notes=(
                            "Se reemplazaron 27 barras"
                        ),
                        first_started_at=datetime(
                            2026,
                            9,
                            18,
                            7,
                            0,
                        ),
                        last_ended_at=datetime(
                            2026,
                            9,
                            18,
                            11,
                            0,
                        ),
                        effective_seconds=(
                            8 * 60 * 60
                        ),
                        elapsed_work_seconds=(
                            4 * 60 * 60
                        ),
                        has_active_session=False,
                        technicians=[
                            SimpleNamespace(
                                person_code="TECH-001",
                                effective_seconds=(
                                    4 * 60 * 60
                                ),
                            ),
                            SimpleNamespace(
                                person_code="TECH-002",
                                effective_seconds=(
                                    4 * 60 * 60
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ],
        operational_activities=[],
    )

    text = DailyReportTextPresenter.present(
        report
    )

    assert "*REPORTE DE ACTIVIDADES*" in text
    assert "*18/09/2026*" in text

    assert "*07:00 - 11:00*" in text

    assert (
        "Reemplazo de barras LED"
        in text
    )

    assert "*OT:* WO-70000" in text

    assert (
        "*Tecnicos:* TECH-001, TECH-002"
        in text
    )

    assert (
        "*Resultado:* Se reemplazaron 27 barras"
        in text
    )

    # El codigo interno de la actividad no
    # necesita aparecer en el texto compartible.
    assert "WO-70000-ACT-001" not in text


def test_should_show_work_order_activity_with_active_session_as_in_progress():

    from app.operations.daily_reports.presenters import (
        DailyReportTextPresenter,
    )

    report = SimpleNamespace(
        report_date=date(
            2026,
            9,
            18,
        ),
        work_orders=[
            SimpleNamespace(
                work_order_code="WO-70001",
                title="Revision electrica",
                asset_code=None,
                activities=[
                    SimpleNamespace(
                        activity_code=(
                            "WO-70001-ACT-001"
                        ),
                        title=(
                            "Revision de tablero"
                        ),
                        status="IN_PROGRESS",
                        completion_notes="",
                        first_started_at=datetime(
                            2026,
                            9,
                            18,
                            7,
                            0,
                        ),
                        last_ended_at=datetime(
                            2026,
                            9,
                            18,
                            9,
                            0,
                        ),
                        effective_seconds=(
                            2 * 60 * 60
                        ),
                        elapsed_work_seconds=(
                            2 * 60 * 60
                        ),
                        has_active_session=True,
                        technicians=[
                            SimpleNamespace(
                                person_code="TECH-001",
                                effective_seconds=(
                                    2 * 60 * 60
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ],
        operational_activities=[],
    )

    text = DailyReportTextPresenter.present(
        report
    )

    assert "*07:00 - En proceso*" in text
    assert "Revision de tablero" in text
    assert "*OT:* WO-70001" in text
    assert "*Tecnicos:* TECH-001" in text

    # 09:00 pertenece a una sesion anterior
    # cerrada. No debe mostrarse como termino
    # mientras exista una sesion activa.
    assert "*07:00 - 09:00*" not in text
