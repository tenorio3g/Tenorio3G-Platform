def build_test_app():
    from app import create_app

    app = create_app()

    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
    )

    return app


def test_daily_report_should_require_authentication():
    app = build_test_app()
    client = app.test_client()

    response = client.get(
        "/operaciones/reporte-diario"
    )

    assert response.status_code == 302

    assert "/login" in response.headers["Location"]


def test_daily_report_should_execute_query_for_current_date(
    monkeypatch,
):
    from datetime import date
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    calls = []

    class DailyReportStub:

        def execute(self, query):
            from types import SimpleNamespace

            calls.append(query)

            return SimpleNamespace(
                report_date=query.report_date,
                work_orders=[],
                operational_activities=[],
                total_work_orders=0,
                total_activities=0,
                completed_activities=0,
                in_progress_activities=0,
                on_hold_activities=0,
                effective_seconds=0,
            )

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "get_daily_operational_report",
        DailyReportStub(),
        raising=False,
    )

    report_date = date(
        2026,
        9,
        18,
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: report_date,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/reporte-diario"
    )

    assert response.status_code == 200

    assert len(calls) == 1

    query = calls[0]

    assert query.report_date == report_date


def test_daily_report_should_render_operational_activity(
    monkeypatch,
):
    from datetime import date, datetime
    from importlib import import_module
    from types import SimpleNamespace

    app = build_test_app()
    client = app.test_client()

    report_date = date(
        2026,
        9,
        18,
    )

    report = SimpleNamespace(
        report_date=report_date,
        work_orders=[],
        operational_activities=[
            SimpleNamespace(
                code="OPA-TEST001",
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
                location_description=(
                    "Perimetro de planta"
                ),
                asset_code=None,
                work_order_code=None,
                status="COMPLETED",
            ),
        ],
        total_work_orders=0,
        total_activities=0,
        completed_activities=0,
        in_progress_activities=0,
        on_hold_activities=0,
        effective_seconds=0,
    )

    class DailyReportStub:

        def execute(self, query):
            return report

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "get_daily_operational_report",
        DailyReportStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: report_date,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/reporte-diario"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "Reporte diario de actividades" in html
    assert "18/09/2026" in html
    assert "OPA-TEST001" in html

    assert (
        "Revision de alumbrado exterior"
        in html
    )

    assert "07:00" in html
    assert "09:00" in html
    assert "Completada" in html

    assert (
        "Alumbrado revisado correctamente"
        in html
    )

    assert "EXTERIOR" in html
    assert "Perimetro de planta" in html


def test_daily_report_should_render_open_operational_activity(
    monkeypatch,
):
    from datetime import date, datetime
    from importlib import import_module
    from types import SimpleNamespace

    app = build_test_app()
    client = app.test_client()

    report_date = date(
        2026,
        9,
        18,
    )

    report = SimpleNamespace(
        report_date=report_date,
        work_orders=[],
        operational_activities=[
            SimpleNamespace(
                code="OPA-OPEN001",
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
        total_work_orders=0,
        total_activities=0,
        completed_activities=0,
        in_progress_activities=0,
        on_hold_activities=0,
        effective_seconds=0,
    )

    class DailyReportStub:

        def execute(self, query):
            return report

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "get_daily_operational_report",
        DailyReportStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: report_date,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/reporte-diario"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "OPA-OPEN001" in html

    assert (
        "Revision de alimentacion de camaras"
        in html
    )

    assert "11:30" in html
    assert "En proceso" in html

    assert "SISTEMAS" in html
    assert "MD2" in html

    # No debe inventarse una hora de termino.
    assert "11:30 - 12:" not in html


def test_daily_report_should_render_work_order_activity(
    monkeypatch,
):
    from datetime import date, datetime
    from importlib import import_module
    from types import SimpleNamespace

    app = build_test_app()
    client = app.test_client()

    report_date = date(
        2026,
        9,
        18,
    )

    report = SimpleNamespace(
        report_date=report_date,
        work_orders=[
            SimpleNamespace(
                work_order_code="WO-70000",
                title=(
                    "Mantenimiento de alumbrado MD1"
                ),
                asset_code="ALUM-MD1",
                activities=[
                    SimpleNamespace(
                        activity_code="WO-70000-ACT-001",
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
        total_work_orders=1,
        total_activities=1,
        completed_activities=1,
        in_progress_activities=0,
        on_hold_activities=0,
        effective_seconds=8 * 60 * 60,
    )

    class DailyReportStub:

        def execute(self, query):
            return report

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "get_daily_operational_report",
        DailyReportStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: report_date,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/reporte-diario"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "Ordenes de trabajo" in html
    assert "WO-70000" in html

    assert (
        "Mantenimiento de alumbrado MD1"
        in html
    )

    assert "ALUM-MD1" in html
    assert "WO-70000-ACT-001" in html
    assert "Reemplazo de barras LED" in html

    assert "07:00" in html
    assert "11:00" in html
    assert "Completada" in html

    assert "TECH-001" in html
    assert "TECH-002" in html

    assert (
        "Se reemplazaron 27 barras"
        in html
    )


def test_daily_report_should_render_work_order_summary(
    monkeypatch,
):
    from datetime import date
    from importlib import import_module
    from types import SimpleNamespace

    app = build_test_app()
    client = app.test_client()

    report_date = date(
        2026,
        9,
        18,
    )

    report = SimpleNamespace(
        report_date=report_date,
        work_orders=[],
        operational_activities=[],
        total_work_orders=3,
        total_activities=7,
        completed_activities=4,
        in_progress_activities=2,
        on_hold_activities=1,
        effective_seconds=(
            10 * 60 * 60
            + 30 * 60
        ),
    )

    class DailyReportStub:

        def execute(self, query):
            return report

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "get_daily_operational_report",
        DailyReportStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: report_date,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/reporte-diario"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "Resumen de ordenes de trabajo" in html
    assert "Ordenes atendidas" in html
    assert ">3<" in html

    assert "Actividades de OT" in html
    assert ">7<" in html

    assert "Completadas" in html
    assert ">4<" in html

    assert "En proceso" in html
    assert ">2<" in html

    assert "En espera" in html
    assert ">1<" in html

    assert "10 h 30 min" in html


def test_daily_report_should_render_shareable_report_text(
    monkeypatch,
):
    from datetime import date, datetime
    from importlib import import_module
    from types import SimpleNamespace

    app = build_test_app()
    client = app.test_client()

    report_date = date(
        2026,
        9,
        18,
    )

    report = SimpleNamespace(
        report_date=report_date,
        work_orders=[],
        operational_activities=[
            SimpleNamespace(
                code="OPA-SHARE01",
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
        ],
        total_work_orders=0,
        total_activities=0,
        completed_activities=0,
        in_progress_activities=0,
        on_hold_activities=0,
        effective_seconds=0,
    )

    class DailyReportStub:

        def execute(self, query):
            return report

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "get_daily_operational_report",
        DailyReportStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: report_date,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/reporte-diario"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "Reporte para compartir" in html
    assert "REPORTE DE ACTIVIDADES" in html
    assert "07:00 - 09:00" in html

    assert (
        "Revision de alumbrado exterior"
        in html
    )

    assert (
        "*Resultado:* Alumbrado revisado correctamente"
        in html
    )

    # El texto compartible no expone el codigo
    # interno de OperationalActivity.
    share_start = html.index(
        "Reporte para compartir"
    )

    share_html = html[share_start:]

    assert "OPA-SHARE01" not in share_html


def test_daily_report_should_render_clean_share_preview(
    monkeypatch,
):
    from datetime import date, datetime
    from importlib import import_module
    from types import SimpleNamespace

    app = build_test_app()
    client = app.test_client()

    report_date = date(
        2026,
        9,
        18,
    )

    report = SimpleNamespace(
        report_date=report_date,
        work_orders=[],
        operational_activities=[
            SimpleNamespace(
                code="OPA-PREVIEW01",
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
                location_description="MD2",
                asset_code=None,
                work_order_code=None,
                status="COMPLETED",
            ),
        ],
        total_work_orders=0,
        total_activities=0,
        completed_activities=0,
        in_progress_activities=0,
        on_hold_activities=0,
        effective_seconds=0,
    )

    class DailyReportStub:

        def execute(self, query):
            return report

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "get_daily_operational_report",
        DailyReportStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: report_date,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/reporte-diario"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert 'id="daily-report-preview"' in html

    assert (
        '<strong>REPORTE DE ACTIVIDADES</strong>'
        in html
    )

    assert (
        "18/09/2026"
        in html
    )

    assert (
        "07:00 - 09:00"
        in html
    )

    assert "<strong>Area:</strong>" in html
    assert "EXTERIOR" in html

    assert "<strong>Ubicacion:</strong>" in html
    assert "MD2" in html

    assert "<strong>Resultado:</strong>" in html

    assert (
        "Alumbrado revisado correctamente"
        in html
    )

    # La fuente destinada al portapapeles
    # conserva la sintaxis de WhatsApp.
    assert (
        'id="shareable-daily-report"'
        in html
    )

    assert (
        "*REPORTE DE ACTIVIDADES*"
        in html
    )

    assert (
        "*07:00 - 09:00*"
        in html
    )

    assert (
        "*Resultado:* "
        "Alumbrado revisado correctamente"
        in html
    )

    assert (
        "Copiar para WhatsApp"
        in html
    )


def test_daily_report_should_render_copy_report_control(
    monkeypatch,
):
    from datetime import date
    from importlib import import_module
    from types import SimpleNamespace

    app = build_test_app()
    client = app.test_client()

    report_date = date(
        2026,
        9,
        18,
    )

    report = SimpleNamespace(
        report_date=report_date,
        work_orders=[],
        operational_activities=[],
        total_work_orders=0,
        total_activities=0,
        completed_activities=0,
        in_progress_activities=0,
        on_hold_activities=0,
        effective_seconds=0,
    )

    class DailyReportStub:

        def execute(self, query):
            return report

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "get_daily_operational_report",
        DailyReportStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: report_date,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/reporte-diario"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert 'id="copy-daily-report"' in html

    assert (
        'id="shareable-daily-report"'
        in html
    )

    assert "Copiar para WhatsApp" in html
