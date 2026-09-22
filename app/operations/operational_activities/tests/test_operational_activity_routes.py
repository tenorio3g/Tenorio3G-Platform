from app import create_app


def build_test_app():
    app = create_app()
    app.config["TESTING"] = True
    return app


def test_new_operational_activity_should_redirect_without_login():
    app = build_test_app()
    client = app.test_client()

    response = client.get(
        "/operaciones/actividades/nueva",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_new_operational_activity_should_render_for_authenticated_user():
    app = build_test_app()
    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/nueva",
    )

    assert response.status_code == 200
    assert b"Nueva actividad operacional" in response.data



def test_new_operational_activity_should_list_work_orders(
    monkeypatch,
):
    app = build_test_app()
    client = app.test_client()

    class WorkOrderStub:

        def __init__(
            self,
            code,
            title,
            status,
        ):
            self.code = code
            self.title = title
            self.status = status

    class ListWorkOrdersResultStub:

        def __init__(self):
            self.work_orders = [
                WorkOrderStub(
                    code="WO-001",
                    title="Revision de alumbrado",
                    status="IN_PROGRESS",
                ),
                WorkOrderStub(
                    code="WO-002",
                    title="Mantenimiento de compresor",
                    status="CLOSED",
                ),
            ]

    class ListWorkOrdersStub:

        def execute(self):
            return ListWorkOrdersResultStub()

    from importlib import import_module

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "list_work_orders",
        ListWorkOrdersStub(),
        raising=False,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/nueva",
    )

    assert response.status_code == 200

    assert b"Sin orden relacionada" in response.data
    assert b"WO-001" in response.data
    assert b"Revision de alumbrado" in response.data
    assert b"WO-002" in response.data
    assert b"Mantenimiento de compresor" in response.data


def test_create_operational_activity_should_reject_unknown_work_order(
    monkeypatch,
):
    app = build_test_app()
    client = app.test_client()

    create_calls = []

    class CreateOperationalActivityStub:

        def execute(self, **kwargs):
            create_calls.append(kwargs)
            return object()

    class GetWorkOrderStub:

        def execute(self, query):
            raise ValueError("work order not found")

    class ListWorkOrdersResultStub:
        work_orders = []

    class ListWorkOrdersStub:

        def execute(self):
            return ListWorkOrdersResultStub()

    from importlib import import_module

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "create_operational_activity",
        CreateOperationalActivityStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "get_work_order",
        GetWorkOrderStub(),
        raising=False,
    )

    monkeypatch.setattr(
        routes_module,
        "list_work_orders",
        ListWorkOrdersStub(),
        raising=False,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.post(
        "/operaciones/actividades/nueva",
        data={
            "description": "Revision de alumbrado",
            "started_at": "2026-09-18T07:00",
            "area": "MD2",
            "work_order_code": "WO-NO-EXISTE",
        },
    )

    assert response.status_code == 200

    assert (
        b"La orden de trabajo seleccionada no existe."
        in response.data
    )

    assert create_calls == []



def test_create_operational_activity_should_redirect_without_login():
    app = build_test_app()
    client = app.test_client()

    response = client.post(
        "/operaciones/actividades/nueva",
        data={
            "description": "Revisi?n de alumbrado",
            "started_at": "2026-09-18T07:00",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_create_operational_activity_should_use_authenticated_person(
    monkeypatch,
):
    app = build_test_app()
    client = app.test_client()

    captured = {}

    class CreatedActivityStub:
        code = "OPA-TEST0001"

    class CreateOperationalActivityStub:

        def execute(self, **kwargs):
            captured.update(kwargs)
            return CreatedActivityStub()

    class GetWorkOrderResultStub:

        class WorkOrderStub:
            code = "71589"

        work_order = WorkOrderStub()

    class GetWorkOrderStub:

        def execute(self, query):
            assert query.code == "71589"
            return GetWorkOrderResultStub()

    from importlib import import_module

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "create_operational_activity",
        CreateOperationalActivityStub(),
        raising=False,
    )

    monkeypatch.setattr(
        routes_module,
        "get_work_order",
        GetWorkOrderStub(),
        raising=False,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "tech-001"
        session["role_code"] = "TECHNICIAN"

    response = client.post(
        "/operaciones/actividades/nueva",
        data={
            "description": "  Revisi?n de alumbrado  ",
            "started_at": "2026-09-18T07:00",
            "area": "MD2",
            "location_description": "Producci?n",
            "asset_code": "LAMP-001",
            "work_order_code": "71589",
            "created_by_person_code": "FAKE-USER",
            "code": "OPA-FAKE000",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith(
        "/operaciones/actividades/"
        "OPA-TEST0001/registrada"
    )

    assert captured["description"] == (
        "  Revisi?n de alumbrado  "
    )
    assert captured["started_at"].isoformat() == (
        "2026-09-18T07:00:00"
    )
    assert captured["area"] == "MD2"
    assert captured["location_description"] == "Producci?n"
    assert captured["asset_code"] == "LAMP-001"
    assert captured["work_order_code"] == "71589"

    assert captured["created_by_person_code"] == "TECH-001"

    assert "code" not in captured


def test_create_operational_activity_should_render_validation_error(
    monkeypatch,
):
    app = build_test_app()
    client = app.test_client()

    calls = []

    class CreateOperationalActivityStub:

        def execute(self, **kwargs):
            calls.append(kwargs)
            raise ValueError("description is required")

    from importlib import import_module

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "create_operational_activity",
        CreateOperationalActivityStub(),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.post(
        "/operaciones/actividades/nueva",
        data={
            "description": "",
            "started_at": "2026-09-18T07:00",
            "area": "MD2",
            "location_description": "Produccion",
        },
    )

    assert response.status_code == 200
    assert b"description is required" in response.data
    assert len(calls) == 1


def test_create_operational_activity_should_reject_invalid_started_at(
    monkeypatch,
):
    app = build_test_app()
    client = app.test_client()

    calls = []

    class CreateOperationalActivityStub:

        def execute(self, **kwargs):
            calls.append(kwargs)
            return object()

    from importlib import import_module

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "create_operational_activity",
        CreateOperationalActivityStub(),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.post(
        "/operaciones/actividades/nueva",
        data={
            "description": "Revision de alumbrado",
            "started_at": "fecha-invalida",
            "area": "MD2",
        },
    )

    assert response.status_code == 200
    assert len(calls) == 0


def test_create_operational_activity_should_show_success_confirmation(
    monkeypatch,
):
    app = build_test_app()
    client = app.test_client()

    class CreatedActivityStub:
        code = "OPA-ABC12345"

    class CreateOperationalActivityStub:

        def execute(self, **kwargs):
            return CreatedActivityStub()

    from importlib import import_module

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "create_operational_activity",
        CreateOperationalActivityStub(),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.post(
        "/operaciones/actividades/nueva",
        data={
            "description": "Actividad de prueba",
            "started_at": "2026-09-17T10:00",
            "area": "MD2",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert (
        b"Actividad registrada correctamente"
        in response.data
    )
    assert b"OPA-ABC12345" in response.data


def test_today_operational_activities_should_redirect_without_login():
    app = build_test_app()
    client = app.test_client()

    response = client.get(
        "/operaciones/actividades/hoy",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_today_operational_activities_should_query_repository_for_current_date(
    monkeypatch,
):
    from datetime import date
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    requested_dates = []

    class OperationalActivityRepositoryStub:

        def list_by_date(self, report_date):
            requested_dates.append(report_date)
            return []

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
        raising=False,
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: date(2026, 9, 17),
        raising=False,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/hoy",
    )

    assert response.status_code == 200
    assert requested_dates == [
        date(2026, 9, 17)
    ]


def test_today_operational_activities_should_render_activity_details(
    monkeypatch,
):
    from datetime import date, datetime
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    class StatusStub:
        value = "IN_PROGRESS"

    class OperationalActivityStub:
        code = "OPA-ABC12345"
        description = "Revision de alumbrado MD2"
        started_at = datetime(
            2026,
            9,
            17,
            7,
            30,
        )
        ended_at = None
        area = "MD2"
        location_description = "Produccion"
        asset_code = "LAMP-001"
        work_order_code = None
        status = StatusStub()

    class OperationalActivityRepositoryStub:

        def list_by_date(self, report_date):
            assert report_date == date(
                2026,
                9,
                17,
            )
            return [
                OperationalActivityStub()
            ]

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: date(2026, 9, 17),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/hoy",
    )

    assert response.status_code == 200

    assert b"Actividades de hoy" in response.data
    assert b"OPA-ABC12345" in response.data
    assert b"Revision de alumbrado MD2" in response.data
    assert b"07:30" in response.data
    assert b"MD2" in response.data
    assert b"Produccion" in response.data
    assert b"En proceso" in response.data


def test_today_operational_activities_should_render_completed_activity(
    monkeypatch,
):
    from datetime import date, datetime
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    class StatusStub:
        value = "COMPLETED"

    class OperationalActivityStub:
        code = "OPA-DONE0001"
        description = "Mantenimiento terminado"
        started_at = datetime(
            2026,
            9,
            17,
            8,
            0,
        )
        ended_at = datetime(
            2026,
            9,
            17,
            10,
            30,
        )
        area = "MD2"
        location_description = "Produccion"
        asset_code = None
        work_order_code = None
        status = StatusStub()

    class OperationalActivityRepositoryStub:

        def list_by_date(self, report_date):
            return [
                OperationalActivityStub()
            ]

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: date(2026, 9, 17),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/hoy",
    )

    assert response.status_code == 200
    assert b"OPA-DONE0001" in response.data
    assert b"Mantenimiento terminado" in response.data
    assert b"Completada" in response.data
    assert b"10:30" in response.data


def test_today_operational_activities_should_render_empty_state(
    monkeypatch,
):
    from datetime import date
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    requested_dates = []

    class OperationalActivityRepositoryStub:

        def list_by_date(self, report_date):
            requested_dates.append(report_date)
            return []

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: date(2026, 9, 17),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/hoy",
    )

    assert response.status_code == 200

    assert requested_dates == [
        date(2026, 9, 17)
    ]

    assert (
        b"No hay actividades operacionales"
        in response.data
    )

    assert b"+ Nueva actividad" in response.data


def test_today_operational_activities_should_identify_carried_activity(
    monkeypatch,
):
    from datetime import date, datetime
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    class StatusStub:
        value = "IN_PROGRESS"

    class OperationalActivityStub:
        code = "OPA-CARRY001"
        description = "Actividad pendiente de dias anteriores"
        started_at = datetime(
            2026,
            9,
            14,
            10,
            0,
        )
        ended_at = None
        area = "MD2"
        location_description = "Produccion"
        asset_code = None
        work_order_code = None
        status = StatusStub()

    class OperationalActivityRepositoryStub:

        def list_by_date(self, report_date):
            assert report_date == date(
                2026,
                9,
                17,
            )
            return [
                OperationalActivityStub()
            ]

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: date(2026, 9, 17),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/hoy",
    )

    assert response.status_code == 200

    assert b"OPA-CARRY001" in response.data

    assert b"Iniciada el" in response.data
    assert b"14/09/2026" in response.data


def test_today_operational_activities_should_not_identify_same_day_activity_as_carried(
    monkeypatch,
):
    from datetime import date, datetime
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    class StatusStub:
        value = "IN_PROGRESS"

    class OperationalActivityStub:
        code = "OPA-TODAY001"
        description = "Actividad iniciada hoy"
        started_at = datetime(
            2026,
            9,
            17,
            9,
            0,
        )
        ended_at = None
        area = "MD2"
        location_description = "Produccion"
        asset_code = None
        work_order_code = None
        status = StatusStub()

    class OperationalActivityRepositoryStub:

        def list_by_date(self, report_date):
            assert report_date == date(
                2026,
                9,
                17,
            )
            return [
                OperationalActivityStub()
            ]

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: date(2026, 9, 17),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/hoy",
    )

    assert response.status_code == 200
    assert b"OPA-TODAY001" in response.data
    assert b"Actividad iniciada hoy" in response.data

    assert b"Iniciada el" not in response.data


def test_complete_operational_activity_should_redirect_without_login():
    app = build_test_app()
    client = app.test_client()

    response = client.get(
        "/operaciones/actividades/"
        "OPA-TEST0001/finalizar",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_complete_operational_activity_should_load_activity_by_code(
    monkeypatch,
):
    from datetime import datetime
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    requested_codes = []

    class StatusStub:
        value = "IN_PROGRESS"

    class OperationalActivityStub:
        code = "OPA-TEST0001"
        description = "Revision de alumbrado"
        started_at = datetime(
            2026,
            9,
            18,
            7,
            30,
        )
        ended_at = None
        area = "MD2"
        location_description = "Produccion"
        asset_code = "LAMP-001"
        work_order_code = None
        status = StatusStub()

    class OperationalActivityRepositoryStub:

        def get_by_code(self, code):
            requested_codes.append(code)
            return OperationalActivityStub()

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/"
        "opa-test0001/finalizar",
    )

    assert response.status_code == 200

    assert requested_codes == [
        "OPA-TEST0001"
    ]

    assert b"Finalizar actividad" in response.data
    assert b"OPA-TEST0001" in response.data
    assert b"Revision de alumbrado" in response.data
    assert b"07:30" in response.data
    assert b"MD2" in response.data
    assert b"Produccion" in response.data


def test_complete_operational_activity_should_return_404_when_activity_not_found(
    monkeypatch,
):
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    requested_codes = []

    class OperationalActivityRepositoryStub:

        def get_by_code(self, code):
            requested_codes.append(code)
            return None

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/"
        "opa-missing/finalizar",
    )

    assert requested_codes == [
        "OPA-MISSING"
    ]

    assert response.status_code == 404


def test_complete_operational_activity_should_return_409_when_activity_is_already_completed(
    monkeypatch,
):
    from datetime import datetime
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    class StatusStub:
        value = "COMPLETED"

    class OperationalActivityStub:
        code = "OPA-TEST0001"
        description = "Revision de alumbrado"
        started_at = datetime(
            2026,
            9,
            18,
            7,
            30,
        )
        ended_at = datetime(
            2026,
            9,
            18,
            9,
            0,
        )
        area = "MD2"
        location_description = "Produccion"
        asset_code = "LAMP-001"
        work_order_code = None
        status = StatusStub()

    class OperationalActivityRepositoryStub:

        def get_by_code(self, code):
            return OperationalActivityStub()

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/"
        "OPA-TEST0001/finalizar",
    )

    assert response.status_code == 409

    assert b'name="ended_at"' not in response.data
    assert b'name="result_notes"' not in response.data


def test_complete_operational_activity_post_should_redirect_without_login():

    app = build_test_app()
    client = app.test_client()

    response = client.post(
        "/operaciones/actividades/"
        "OPA-TEST0001/finalizar",
        data={
            "ended_at": "2026-09-18T09:30",
            "result_notes": "Trabajo terminado",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_complete_operational_activity_post_should_execute_use_case_with_authenticated_actor(
    monkeypatch,
):
    from datetime import datetime
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    calls = []

    class StatusStub:
        value = "IN_PROGRESS"

    class OperationalActivityStub:
        code = "OPA-TEST0001"
        description = "Revision de alumbrado"
        started_at = datetime(
            2026,
            9,
            18,
            7,
            30,
        )
        ended_at = None
        area = "MD2"
        location_description = "Produccion"
        asset_code = "LAMP-001"
        work_order_code = None
        status = StatusStub()

    class OperationalActivityRepositoryStub:

        def get_by_code(self, code):
            return OperationalActivityStub()

    class CompleteOperationalActivityStub:

        def execute(self, **kwargs):
            calls.append(kwargs)
            return OperationalActivityStub()

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "complete_operational_activity",
        CompleteOperationalActivityStub(),
        raising=False,
    )

    fixed_completed_at = datetime(
        2026,
        9,
        18,
        10,
        15,
    )

    monkeypatch.setattr(
        routes_module,
        "current_datetime",
        lambda: fixed_completed_at,
        raising=False,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.post(
        "/operaciones/actividades/"
        "opa-test0001/finalizar",
        data={
            "ended_at": "2026-09-18T09:30",
            "result_notes": "Trabajo terminado",
            "completed_by_person_code": "HACK-999",
        },
        follow_redirects=False,
    )

    assert calls == [
        {
            "code": "OPA-TEST0001",
            "ended_at": datetime(
                2026,
                9,
                18,
                9,
                30,
            ),
            "result_notes": "Trabajo terminado",
            "completed_at": fixed_completed_at,
            "completed_by_person_code": "TECH-001",
        }
    ]

    assert response.status_code == 302

    assert response.headers["Location"].endswith(
        "/operaciones/actividades/hoy"
    )


def test_complete_operational_activity_post_should_return_400_when_ended_at_is_invalid(
    monkeypatch,
):
    from datetime import datetime
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    calls = []

    class StatusStub:
        value = "IN_PROGRESS"

    class OperationalActivityStub:
        code = "OPA-TEST0001"
        description = "Revision de alumbrado"
        started_at = datetime(
            2026,
            9,
            18,
            7,
            30,
        )
        ended_at = None
        area = "MD2"
        location_description = "Produccion"
        asset_code = "LAMP-001"
        work_order_code = None
        status = StatusStub()

    class OperationalActivityRepositoryStub:

        def get_by_code(self, code):
            return OperationalActivityStub()

    class CompleteOperationalActivityStub:

        def execute(self, **kwargs):
            calls.append(kwargs)

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "complete_operational_activity",
        CompleteOperationalActivityStub(),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.post(
        "/operaciones/actividades/"
        "OPA-TEST0001/finalizar",
        data={
            "ended_at": "fecha-invalida",
            "result_notes": "Trabajo terminado",
        },
    )

    assert response.status_code == 400

    assert calls == []

    assert b"Finalizar actividad" in response.data
    assert b"OPA-TEST0001" in response.data
    assert b"Revision de alumbrado" in response.data

    assert b"fecha-invalida" in response.data
    assert b"Trabajo terminado" in response.data


def test_complete_operational_activity_post_should_return_400_when_use_case_rejects_completion(
    monkeypatch,
):
    from datetime import datetime
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    calls = []

    class StatusStub:
        value = "IN_PROGRESS"

    class OperationalActivityStub:
        code = "OPA-TEST0001"
        description = "Revision de alumbrado"
        started_at = datetime(
            2026,
            9,
            18,
            7,
            30,
        )
        ended_at = None
        area = "MD2"
        location_description = "Produccion"
        asset_code = "LAMP-001"
        work_order_code = None
        status = StatusStub()

    class OperationalActivityRepositoryStub:

        def get_by_code(self, code):
            return OperationalActivityStub()

    class CompleteOperationalActivityStub:

        def execute(self, **kwargs):
            calls.append(kwargs)
            raise ValueError(
                "ended_at cannot be before started_at"
            )

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        OperationalActivityRepositoryStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "complete_operational_activity",
        CompleteOperationalActivityStub(),
    )

    fixed_completed_at = datetime(
        2026,
        9,
        18,
        10,
        15,
    )

    monkeypatch.setattr(
        routes_module,
        "current_datetime",
        lambda: fixed_completed_at,
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.post(
        "/operaciones/actividades/"
        "OPA-TEST0001/finalizar",
        data={
            "ended_at": "2026-09-18T06:30",
            "result_notes": "Trabajo terminado",
        },
    )

    assert len(calls) == 1

    assert calls[0][
        "completed_by_person_code"
    ] == "TECH-001"

    assert response.status_code == 400

    assert b"Finalizar actividad" in response.data
    assert b"OPA-TEST0001" in response.data

    assert (
        b"ended_at cannot be before started_at"
        in response.data
    )

    assert b"2026-09-18T06:30" in response.data
    assert b"Trabajo terminado" in response.data


def test_today_operational_activities_should_show_complete_link_only_for_in_progress_activity(
    monkeypatch,
):
    from datetime import date, datetime
    from importlib import import_module

    app = build_test_app()
    client = app.test_client()

    class InProgressStatusStub:
        value = "IN_PROGRESS"

    class CompletedStatusStub:
        value = "COMPLETED"

    class InProgressActivityStub:
        code = "OPA-OPEN0001"
        description = "Actividad abierta"
        started_at = datetime(
            2026,
            9,
            18,
            8,
            0,
        )
        ended_at = None
        area = "MD2"
        location_description = ""
        asset_code = None
        work_order_code = None
        status = InProgressStatusStub()

    class CompletedActivityStub:
        code = "OPA-DONE0001"
        description = "Actividad terminada"
        started_at = datetime(
            2026,
            9,
            18,
            7,
            0,
        )
        ended_at = datetime(
            2026,
            9,
            18,
            9,
            0,
        )
        area = "MD1"
        location_description = ""
        asset_code = None
        work_order_code = None
        status = CompletedStatusStub()

    class RepositoryStub:

        def list_by_date(self, report_date):
            return [
                InProgressActivityStub(),
                CompletedActivityStub(),
            ]

    routes_module = import_module(
        "app.operations.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "operational_activity_repository",
        RepositoryStub(),
    )

    monkeypatch.setattr(
        routes_module,
        "current_date",
        lambda: date(2026, 9, 18),
    )

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["person_code"] = "TECH-001"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/operaciones/actividades/hoy"
    )

    assert response.status_code == 200

    html = response.get_data(as_text=True)

    open_url = (
        "/operaciones/actividades/"
        "OPA-OPEN0001/finalizar"
    )

    completed_url = (
        "/operaciones/actividades/"
        "OPA-DONE0001/finalizar"
    )

    assert open_url in html
    assert completed_url not in html
    assert "Finalizar actividad" in html

