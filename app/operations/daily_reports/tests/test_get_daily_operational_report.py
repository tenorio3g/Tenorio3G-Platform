from datetime import date, datetime, time, timedelta

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)
from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)
from app.domains.work_orders.entities import (
    WorkOrder,
)
from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)
from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)
from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)
from app.operations.daily_reports.queries import (
    GetDailyOperationalReport,
    GetDailyOperationalReportQuery,
)
from app.operations.operational_activities.entities import (
    OperationalActivity,
    OperationalActivitySource,
)


class StubWorkOrderRepository:

    def __init__(
        self,
        work_orders=None,
    ):
        self._work_orders = list(
            work_orders or []
        )

    def list_all(
        self,
    ):
        return list(
            self._work_orders
        )


class StubActivityRepository:

    def __init__(
        self,
        activities=None,
    ):
        self._activities = list(
            activities or []
        )

    def list_by_work_order(
        self,
        work_order_code,
    ):
        return [
            activity
            for activity in self._activities
            if activity.work_order_code
            == work_order_code
        ]


class StubWorkSessionRepository:

    def __init__(
        self,
        work_sessions=None,
    ):
        self._work_sessions = list(
            work_sessions or []
        )

    def list_by_activity(
        self,
        activity_code,
    ):
        return [
            work_session
            for work_session in self._work_sessions
            if work_session.activity_code
            == activity_code
        ]


class StubOperationalActivityRepository:

    def __init__(
        self,
        operational_activities=None,
    ):
        self._operational_activities = list(
            operational_activities or []
        )

    def list_by_date(
        self,
        report_date,
    ):
        day_start = datetime.combine(
            report_date,
            time.min,
        )

        day_end = (
            day_start
            + timedelta(days=1)
        )

        return [
            activity
            for activity in self._operational_activities
            if (
                activity.started_at < day_end
                and (
                    activity.ended_at is None
                    or activity.ended_at > day_start
                )
            )
        ]


def create_use_case(
    work_orders=None,
    activities=None,
    work_sessions=None,
    operational_activities=None,
):
    return GetDailyOperationalReport(
        work_order_repository=(
            StubWorkOrderRepository(
                work_orders,
            )
        ),
        activity_repository=(
            StubActivityRepository(
                activities,
            )
        ),
        work_session_repository=(
            StubWorkSessionRepository(
                work_sessions,
            )
        ),
        operational_activity_repository=(
            StubOperationalActivityRepository(
                operational_activities,
            )
        ),
    )


def test_should_return_empty_report_when_day_has_no_work():

    use_case = create_use_case()

    result = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    assert result.report_date == date(
        2026,
        9,
        16,
    )

    assert result.work_orders == []
    assert result.total_work_orders == 0
    assert result.total_activities == 0
    assert result.completed_activities == 0
    assert result.in_progress_activities == 0
    assert result.on_hold_activities == 0
    assert result.effective_seconds == 0


def test_should_include_work_session_fully_inside_report_day():

    work_order = WorkOrder(
        code="WO-001",
        title="Mantenimiento de alumbrado",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-001",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            15,
            10,
            0,
        ),
        status=WorkOrderStatus.IN_PROGRESS,
    )

    activity = WorkOrderActivity(
        code="ACT-001",
        work_order_code="WO-001",
        title="Reemplazar barras LED",
        responsible_person_code="TECH-001",
        status=ActivityStatus.IN_PROGRESS,
        started_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
    )

    work_session = WorkSession(
        code="WS-001",
        work_order_code="WO-001",
        activity_code="ACT-001",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            16,
            9,
            30,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
        created_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[
            work_session,
        ],
    )

    result = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    assert result.total_work_orders == 1
    assert result.total_activities == 1
    assert result.completed_activities == 0
    assert result.in_progress_activities == 1
    assert result.on_hold_activities == 0
    assert result.effective_seconds == 5400

    assert len(
        result.work_orders
    ) == 1



def test_should_clip_work_session_that_crosses_midnight():

    work_order = WorkOrder(
        code="WO-002",
        title="Trabajo nocturno",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-002",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            16,
            20,
            0,
        ),
        status=WorkOrderStatus.IN_PROGRESS,
    )

    activity = WorkOrderActivity(
        code="ACT-002",
        work_order_code="WO-002",
        title="Mantenimiento nocturno",
        responsible_person_code="TECH-001",
        status=ActivityStatus.IN_PROGRESS,
        started_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
    )

    work_session = WorkSession(
        code="WS-002",
        work_order_code="WO-002",
        activity_code="ACT-002",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
        ended_at=datetime(
            2026,
            9,
            17,
            1,
            30,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
        created_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[
            work_session,
        ],
    )

    report_day_16 = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    report_day_17 = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                17,
            ),
        )
    )

    assert report_day_16.total_work_orders == 1
    assert report_day_16.total_activities == 1
    assert report_day_16.effective_seconds == 1800

    activity_day_16 = (
        report_day_16
        .work_orders[0]
        .activities[0]
    )

    assert activity_day_16.first_started_at == datetime(
        2026,
        9,
        16,
        23,
        30,
    )

    assert activity_day_16.last_ended_at == datetime(
        2026,
        9,
        17,
        0,
        0,
    )

    assert activity_day_16.elapsed_work_seconds == 1800

    assert report_day_17.total_work_orders == 1
    assert report_day_17.total_activities == 1
    assert report_day_17.effective_seconds == 5400

    activity_day_17 = (
        report_day_17
        .work_orders[0]
        .activities[0]
    )

    assert activity_day_17.first_started_at == datetime(
        2026,
        9,
        17,
        0,
        0,
    )

    assert activity_day_17.last_ended_at == datetime(
        2026,
        9,
        17,
        1,
        30,
    )

    assert activity_day_17.elapsed_work_seconds == 5400



def test_should_include_activity_completed_during_day_without_work_sessions():

    work_order = WorkOrder(
        code="WO-003",
        title="Reporte de mantenimiento",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-003",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            16,
            7,
            0,
        ),
        status=WorkOrderStatus.IN_PROGRESS,
    )

    activity = WorkOrderActivity(
        code="ACT-003",
        work_order_code="WO-003",
        title="Realizar reporte diario",
        responsible_person_code="TECH-001",
        status=ActivityStatus.COMPLETED,
        started_at=datetime(
            2026,
            9,
            16,
            10,
            0,
        ),
        completed_at=datetime(
            2026,
            9,
            16,
            10,
            30,
        ),
        completion_notes=(
            "Se realiz? el reporte diario "
            "de las actividades."
        ),
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[],
    )

    result = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    assert result.total_work_orders == 1
    assert result.total_activities == 1
    assert result.completed_activities == 1
    assert result.in_progress_activities == 0
    assert result.on_hold_activities == 0
    assert result.effective_seconds == 0

    daily_activity = (
        result
        .work_orders[0]
        .activities[0]
    )

    assert daily_activity.activity_code == "ACT-003"

    assert (
        daily_activity.completion_notes
        == "Se realiz? el reporte diario "
        "de las actividades."
    )

    assert daily_activity.effective_seconds == 0
    assert daily_activity.first_started_at is None
    assert daily_activity.last_ended_at is None
    assert daily_activity.technicians == []



def test_should_exclude_activity_unrelated_to_report_day():

    work_order = WorkOrder(
        code="WO-004",
        title="Mantenimiento anterior",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-004",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            15,
            7,
            0,
        ),
        status=WorkOrderStatus.COMPLETED,
    )

    activity = WorkOrderActivity(
        code="ACT-004",
        work_order_code="WO-004",
        title="Trabajo del d?a anterior",
        responsible_person_code="TECH-001",
        status=ActivityStatus.COMPLETED,
        started_at=datetime(
            2026,
            9,
            15,
            8,
            0,
        ),
        completed_at=datetime(
            2026,
            9,
            15,
            9,
            0,
        ),
        completion_notes=(
            "Trabajo realizado el d?a anterior."
        ),
    )

    work_session = WorkSession(
        code="WS-004",
        work_order_code="WO-004",
        activity_code="ACT-004",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            15,
            8,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            15,
            9,
            0,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            15,
            8,
            0,
        ),
        created_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[
            work_session,
        ],
    )

    result = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    assert result.total_work_orders == 0
    assert result.total_activities == 0
    assert result.completed_activities == 0
    assert result.in_progress_activities == 0
    assert result.on_hold_activities == 0
    assert result.effective_seconds == 0
    assert result.work_orders == []


def test_should_aggregate_work_time_by_technician():

    work_order = WorkOrder(
        code="WO-005",
        title="Mantenimiento con varios t?cnicos",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-005",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            16,
            7,
            0,
        ),
        status=WorkOrderStatus.IN_PROGRESS,
    )

    activity = WorkOrderActivity(
        code="ACT-005",
        work_order_code="WO-005",
        title="Trabajo con varios t?cnicos",
        responsible_person_code="TECH-001",
        status=ActivityStatus.IN_PROGRESS,
        started_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
    )

    work_session_1 = WorkSession(
        code="WS-005-A",
        work_order_code="WO-005",
        activity_code="ACT-005",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            16,
            9,
            0,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
        created_by_person_code="TECH-001",
    )

    work_session_2 = WorkSession(
        code="WS-005-B",
        work_order_code="WO-005",
        activity_code="ACT-005",
        person_code="TECH-002",
        started_at=datetime(
            2026,
            9,
            16,
            8,
            30,
        ),
        ended_at=datetime(
            2026,
            9,
            16,
            9,
            30,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            8,
            30,
        ),
        created_by_person_code="TECH-002",
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[
            work_session_1,
            work_session_2,
        ],
    )

    result = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    assert result.total_work_orders == 1
    assert result.total_activities == 1
    assert result.in_progress_activities == 1

    # 1 h de TECH-001 + 1 h de TECH-002.
    assert result.effective_seconds == 7200

    daily_activity = (
        result
        .work_orders[0]
        .activities[0]
    )

    assert daily_activity.first_started_at == datetime(
        2026,
        9,
        16,
        8,
        0,
    )

    assert daily_activity.last_ended_at == datetime(
        2026,
        9,
        16,
        9,
        30,
    )

    assert daily_activity.effective_seconds == 7200

    assert len(daily_activity.technicians) == 2

    technicians_by_code = {
        technician.person_code: technician
        for technician in daily_activity.technicians
    }

    assert set(technicians_by_code) == {
        "TECH-001",
        "TECH-002",
    }

    assert (
        technicians_by_code[
            "TECH-001"
        ].effective_seconds
        == 3600
    )

    assert (
        technicians_by_code[
            "TECH-002"
        ].effective_seconds
        == 3600
    )


def test_should_aggregate_multiple_sessions_from_same_technician():

    work_order = WorkOrder(
        code="WO-006",
        title="Mantenimiento con sesiones m?ltiples",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-006",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            16,
            7,
            0,
        ),
        status=WorkOrderStatus.IN_PROGRESS,
    )

    activity = WorkOrderActivity(
        code="ACT-006",
        work_order_code="WO-006",
        title="Trabajo en dos periodos",
        responsible_person_code="TECH-001",
        status=ActivityStatus.IN_PROGRESS,
        started_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
    )

    work_session_1 = WorkSession(
        code="WS-006-A",
        work_order_code="WO-006",
        activity_code="ACT-006",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            16,
            9,
            0,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
        created_by_person_code="TECH-001",
    )

    work_session_2 = WorkSession(
        code="WS-006-B",
        work_order_code="WO-006",
        activity_code="ACT-006",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            16,
            10,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            16,
            10,
            30,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            10,
            0,
        ),
        created_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[
            work_session_1,
            work_session_2,
        ],
    )

    result = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    assert result.total_work_orders == 1
    assert result.total_activities == 1
    assert result.effective_seconds == 5400

    daily_activity = (
        result
        .work_orders[0]
        .activities[0]
    )

    assert daily_activity.effective_seconds == 5400

    assert daily_activity.first_started_at == datetime(
        2026,
        9,
        16,
        8,
        0,
    )

    assert daily_activity.last_ended_at == datetime(
        2026,
        9,
        16,
        10,
        30,
    )

    assert len(daily_activity.technicians) == 1

    technician = daily_activity.technicians[0]

    assert technician.person_code == "TECH-001"
    assert technician.effective_seconds == 5400


def test_should_calculate_elapsed_work_time_without_double_counting_overlaps_or_gaps():

    work_order = WorkOrder(
        code="WO-007",
        title="Mantenimiento con traslapes y pausas",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-007",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            16,
            7,
            0,
        ),
        status=WorkOrderStatus.IN_PROGRESS,
    )

    activity = WorkOrderActivity(
        code="ACT-007",
        work_order_code="WO-007",
        title="Trabajo con traslapes y pausas",
        responsible_person_code="TECH-001",
        status=ActivityStatus.IN_PROGRESS,
        started_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
    )

    work_session_1 = WorkSession(
        code="WS-007-A",
        work_order_code="WO-007",
        activity_code="ACT-007",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            16,
            9,
            0,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
        created_by_person_code="TECH-001",
    )

    work_session_2 = WorkSession(
        code="WS-007-B",
        work_order_code="WO-007",
        activity_code="ACT-007",
        person_code="TECH-002",
        started_at=datetime(
            2026,
            9,
            16,
            8,
            30,
        ),
        ended_at=datetime(
            2026,
            9,
            16,
            9,
            30,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            8,
            30,
        ),
        created_by_person_code="TECH-002",
    )

    work_session_3 = WorkSession(
        code="WS-007-C",
        work_order_code="WO-007",
        activity_code="ACT-007",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            16,
            10,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            16,
            10,
            30,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            10,
            0,
        ),
        created_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[
            work_session_1,
            work_session_2,
            work_session_3,
        ],
    )

    result = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    assert result.total_work_orders == 1
    assert result.total_activities == 1

    daily_activity = (
        result
        .work_orders[0]
        .activities[0]
    )

    # Segundos-persona:
    # 3600 + 3600 + 1800 = 9000.
    assert daily_activity.effective_seconds == 9000
    assert result.effective_seconds == 9000

    # Uni?n temporal:
    # 08:00-09:30 = 5400
    # 10:00-10:30 = 1800
    # Total = 7200.
    assert daily_activity.elapsed_work_seconds == 7200

    assert daily_activity.first_started_at == datetime(
        2026,
        9,
        16,
        8,
        0,
    )

    assert daily_activity.last_ended_at == datetime(
        2026,
        9,
        16,
        10,
        30,
    )

    technicians_by_code = {
        technician.person_code: technician
        for technician in daily_activity.technicians
    }

    assert (
        technicians_by_code[
            "TECH-001"
        ].effective_seconds
        == 5400
    )

    assert (
        technicians_by_code[
            "TECH-002"
        ].effective_seconds
        == 3600
    )

def test_should_include_activity_with_active_session_without_counting_open_time():

    work_order = WorkOrder(
        code="WO-008",
        title="Trabajo con sesi?n activa",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-008",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            16,
            13,
            0,
        ),
        status=WorkOrderStatus.IN_PROGRESS,
    )

    activity = WorkOrderActivity(
        code="ACT-008",
        work_order_code="WO-008",
        title="Revisi?n de tablero",
        responsible_person_code="TECH-001",
        status=ActivityStatus.IN_PROGRESS,
        started_at=datetime(
            2026,
            9,
            16,
            14,
            20,
        ),
    )

    active_session = WorkSession(
        code="WS-008",
        work_order_code="WO-008",
        activity_code="ACT-008",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            16,
            14,
            20,
        ),
        ended_at=None,
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            14,
            20,
        ),
        created_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[
            active_session,
        ],
    )

    report = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    assert report.total_work_orders == 1
    assert report.total_activities == 1
    assert report.in_progress_activities == 1

    assert report.effective_seconds == 0

    daily_activity = (
        report
        .work_orders[0]
        .activities[0]
    )

    assert daily_activity.activity_code == "ACT-008"
    assert daily_activity.status == "IN_PROGRESS"

    assert daily_activity.has_active_session is True

    assert daily_activity.first_started_at == datetime(
        2026,
        9,
        16,
        14,
        20,
    )

    assert daily_activity.last_ended_at is None

    assert daily_activity.effective_seconds == 0
    assert daily_activity.elapsed_work_seconds == 0

    assert len(daily_activity.technicians) == 1

    technician = daily_activity.technicians[0]

    assert technician.person_code == "TECH-001"
    assert technician.effective_seconds == 0

def test_should_exclude_active_session_that_starts_after_report_day():

    work_order = WorkOrder(
        code="WO-009",
        title="Trabajo futuro",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-009",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            17,
            7,
            0,
        ),
        status=WorkOrderStatus.IN_PROGRESS,
    )

    activity = WorkOrderActivity(
        code="ACT-009",
        work_order_code="WO-009",
        title="Trabajo del d?a siguiente",
        responsible_person_code="TECH-001",
        status=ActivityStatus.IN_PROGRESS,
        started_at=datetime(
            2026,
            9,
            17,
            8,
            0,
        ),
    )

    active_session = WorkSession(
        code="WS-009",
        work_order_code="WO-009",
        activity_code="ACT-009",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            17,
            8,
            0,
        ),
        ended_at=None,
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            17,
            8,
            0,
        ),
        created_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[
            active_session,
        ],
    )

    report = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    assert report.total_work_orders == 0
    assert report.total_activities == 0
    assert report.in_progress_activities == 0
    assert report.effective_seconds == 0
    assert report.work_orders == []

def test_should_include_active_session_carried_over_from_previous_day():

    work_order = WorkOrder(
        code="WO-010",
        title="Trabajo nocturno activo",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-010",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            16,
            22,
            0,
        ),
        status=WorkOrderStatus.IN_PROGRESS,
    )

    activity = WorkOrderActivity(
        code="ACT-010",
        work_order_code="WO-010",
        title="Mantenimiento nocturno activo",
        responsible_person_code="TECH-001",
        status=ActivityStatus.IN_PROGRESS,
        started_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
    )

    active_session = WorkSession(
        code="WS-010",
        work_order_code="WO-010",
        activity_code="ACT-010",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
        ended_at=None,
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
        created_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[
            active_session,
        ],
    )

    report = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                17,
            ),
        )
    )

    assert report.total_work_orders == 1
    assert report.total_activities == 1
    assert report.in_progress_activities == 1
    assert report.effective_seconds == 0

    daily_activity = (
        report
        .work_orders[0]
        .activities[0]
    )

    assert daily_activity.activity_code == "ACT-010"
    assert daily_activity.has_active_session is True

    assert daily_activity.first_started_at == datetime(
        2026,
        9,
        17,
        0,
        0,
    )

    assert daily_activity.last_ended_at is None

    assert daily_activity.effective_seconds == 0
    assert daily_activity.elapsed_work_seconds == 0

    assert len(daily_activity.technicians) == 1

    technician = daily_activity.technicians[0]

    assert technician.person_code == "TECH-001"
    assert technician.effective_seconds == 0

def test_should_combine_closed_work_and_active_session_in_same_activity():

    work_order = WorkOrder(
        code="WO-011",
        title="Trabajo con relevo de t?cnicos",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code="ASSET-011",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            9,
            16,
            7,
            0,
        ),
        status=WorkOrderStatus.IN_PROGRESS,
    )

    activity = WorkOrderActivity(
        code="ACT-011",
        work_order_code="WO-011",
        title="Diagn?stico y reparaci?n",
        responsible_person_code="TECH-001",
        status=ActivityStatus.IN_PROGRESS,
        started_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
    )

    closed_session = WorkSession(
        code="WS-011-A",
        work_order_code="WO-011",
        activity_code="ACT-011",
        person_code="TECH-001",
        started_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            16,
            9,
            0,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            8,
            0,
        ),
        created_by_person_code="TECH-001",
    )

    active_session = WorkSession(
        code="WS-011-B",
        work_order_code="WO-011",
        activity_code="ACT-011",
        person_code="TECH-002",
        started_at=datetime(
            2026,
            9,
            16,
            10,
            0,
        ),
        ended_at=None,
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            9,
            16,
            10,
            0,
        ),
        created_by_person_code="TECH-002",
    )

    use_case = create_use_case(
        work_orders=[
            work_order,
        ],
        activities=[
            activity,
        ],
        work_sessions=[
            closed_session,
            active_session,
        ],
    )

    report = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    assert report.total_work_orders == 1
    assert report.total_activities == 1
    assert report.in_progress_activities == 1

    assert report.effective_seconds == 3600

    daily_activity = (
        report
        .work_orders[0]
        .activities[0]
    )

    assert daily_activity.has_active_session is True

    assert daily_activity.effective_seconds == 3600
    assert daily_activity.elapsed_work_seconds == 3600

    assert daily_activity.first_started_at == datetime(
        2026,
        9,
        16,
        8,
        0,
    )

    assert daily_activity.last_ended_at == datetime(
        2026,
        9,
        16,
        9,
        0,
    )

    assert len(daily_activity.technicians) == 2

    technician_1 = daily_activity.technicians[0]
    technician_2 = daily_activity.technicians[1]

    assert technician_1.person_code == "TECH-001"
    assert technician_1.effective_seconds == 3600

    assert technician_2.person_code == "TECH-002"
    assert technician_2.effective_seconds == 0



def test_should_include_operational_activity_in_report():

    operational_activity = OperationalActivity(
        code="OP-ACT-001",
        description=(
            "Instalaci?n de m?dem y antenas "
            "en gabinete de inversor"
        ),
        started_at=datetime(
            2026,
            9,
            17,
            7,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            17,
            8,
            30,
        ),
        result_notes=(
            "Instalaci?n terminada"
        ),
        area="Subestaci?n 1",
        location_description=(
            "Gabinete de inversor"
        ),
        work_order_code=None,
        source=(
            OperationalActivitySource.MANUAL
        ),
        created_at=datetime(
            2026,
            9,
            17,
            8,
            35,
        ),
        created_by_person_code="TECH-001",
        completed_at=datetime(
            2026,
            9,
            17,
            8,
            35,
        ),
        completed_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        operational_activities=[
            operational_activity,
        ],
    )

    report = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                17,
            ),
        )
    )

    assert len(
        report.operational_activities
    ) == 1

    daily_activity = (
        report.operational_activities[0]
    )

    assert daily_activity.code == "OP-ACT-001"

    assert daily_activity.description == (
        "Instalaci?n de m?dem y antenas "
        "en gabinete de inversor"
    )

    assert daily_activity.started_at == datetime(
        2026,
        9,
        17,
        7,
        0,
    )

    assert daily_activity.ended_at == datetime(
        2026,
        9,
        17,
        8,
        30,
    )

    assert daily_activity.area == "Subestaci?n 1"

    assert daily_activity.location_description == (
        "Gabinete de inversor"
    )

    assert daily_activity.work_order_code is None

    assert daily_activity.status == "COMPLETED"

    assert daily_activity.result_notes == (
        "Instalaci?n terminada"
    )

    # Los contadores existentes siguen representando
    # ?nicamente actividades formales de Work Orders.
    assert report.total_work_orders == 0
    assert report.total_activities == 0
    assert report.effective_seconds == 0



def test_should_include_cross_midnight_operational_activity_in_both_report_days():

    operational_activity = OperationalActivity(
        code="OP-ACT-002",
        description="Trabajo nocturno",
        started_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
        ended_at=datetime(
            2026,
            9,
            17,
            1,
            0,
        ),
        source=OperationalActivitySource.MANUAL,
        created_at=datetime(
            2026,
            9,
            17,
            1,
            5,
        ),
        created_by_person_code="TECH-001",
        completed_at=datetime(
            2026,
            9,
            17,
            1,
            5,
        ),
        completed_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        operational_activities=[
            operational_activity,
        ],
    )

    report_day_1 = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                16,
            ),
        )
    )

    report_day_2 = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                17,
            ),
        )
    )

    assert [
        item.code
        for item
        in report_day_1.operational_activities
    ] == [
        "OP-ACT-002",
    ]

    assert [
        item.code
        for item
        in report_day_2.operational_activities
    ] == [
        "OP-ACT-002",
    ]


def test_should_include_open_operational_activity_carried_from_previous_day():

    operational_activity = OperationalActivity(
        code="OP-ACT-003",
        description="Actividad operacional abierta",
        started_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
        ended_at=None,
        source=OperationalActivitySource.MANUAL,
        created_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
        created_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        operational_activities=[
            operational_activity,
        ],
    )

    report = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                17,
            ),
        )
    )

    assert len(
        report.operational_activities
    ) == 1

    daily_activity = (
        report.operational_activities[0]
    )

    assert daily_activity.code == "OP-ACT-003"
    assert daily_activity.status == "IN_PROGRESS"
    assert daily_activity.ended_at is None


def test_should_exclude_operational_activity_outside_report_day():

    operational_activity = OperationalActivity(
        code="OP-ACT-004",
        description="Actividad de otro d?a",
        started_at=datetime(
            2026,
            9,
            18,
            8,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            18,
            9,
            0,
        ),
        source=OperationalActivitySource.MANUAL,
        created_at=datetime(
            2026,
            9,
            18,
            9,
            5,
        ),
        created_by_person_code="TECH-001",
        completed_at=datetime(
            2026,
            9,
            18,
            9,
            5,
        ),
        completed_by_person_code="TECH-001",
    )

    use_case = create_use_case(
        operational_activities=[
            operational_activity,
        ],
    )

    report = use_case.execute(
        GetDailyOperationalReportQuery(
            report_date=date(
                2026,
                9,
                17,
            ),
        )
    )

    assert report.operational_activities == []
