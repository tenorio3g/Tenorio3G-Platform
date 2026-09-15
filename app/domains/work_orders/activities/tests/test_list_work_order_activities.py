from datetime import datetime

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.holds.entities import (
    ActivityHold,
)

from app.domains.work_orders.activities.holds.repositories import (
    InMemoryActivityHoldRepository,
)

from app.domains.work_orders.activities.holds.value_objects import (
    ActivityHoldReason,
)

from app.domains.work_orders.activities.repositories import (
    InMemoryWorkOrderActivityRepository,
)

from app.domains.work_orders.activities.use_cases import (
    ListWorkOrderActivities,
    ListWorkOrderActivitiesQuery,
)


def build_use_case():

    activity_repository = (
        InMemoryWorkOrderActivityRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    hold_repository = (
        InMemoryActivityHoldRepository()
    )

    use_case = ListWorkOrderActivities(
        activity_repository,
        person_repository,
        hold_repository,
    )

    return (
        activity_repository,
        person_repository,
        hold_repository,
        use_case,
    )


def create_activity(
    code,
    responsible_person_code,
):

    return WorkOrderActivity(
        code=code,
        work_order_code="WO-001",
        title=f"Actividad {code}",
        responsible_person_code=(
            responsible_person_code
        ),
        estimated_minutes=30,
    )


def test_should_list_work_order_activities():

    (
        activity_repository,
        person_repository,
        _,
        use_case,
    ) = build_use_case()

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
            position="Supervisor",
        )
    )

    activity_repository.save(
        create_activity(
            "ACT-001",
            "55464",
        )
    )

    result = use_case.execute(
        ListWorkOrderActivitiesQuery(
            work_order_code="WO-001"
        )
    )

    assert len(result.items) == 1

    item = result.items[0]

    assert item.activity.code == "ACT-001"

    assert (
        item.responsible_person.code
        == "55464"
    )

    assert (
        item.responsible_person.name
        == "Fortunato"
    )

    assert item.active_hold is None


def test_should_list_multiple_activities():

    (
        activity_repository,
        person_repository,
        _,
        use_case,
    ) = build_use_case()

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
        )
    )

    person_repository.save(
        Person(
            code="12",
            name="Pedro",
        )
    )

    activity_repository.save(
        create_activity(
            "ACT-001",
            "55464",
        )
    )

    activity_repository.save(
        create_activity(
            "ACT-002",
            "12",
        )
    )

    result = use_case.execute(
        ListWorkOrderActivitiesQuery(
            work_order_code="WO-001"
        )
    )

    assert len(result.items) == 2

    assert {
        item.responsible_person.code
        for item in result.items
    } == {
        "55464",
        "12",
    }


def test_should_return_empty_list():

    _, _, _, use_case = build_use_case()

    result = use_case.execute(
        ListWorkOrderActivitiesQuery(
            work_order_code="WO-001"
        )
    )

    assert result.items == []


def test_should_ignore_missing_responsible_person():

    (
        activity_repository,
        _,
        _,
        use_case,
    ) = build_use_case()

    activity_repository.save(
        create_activity(
            "ACT-001",
            "99999",
        )
    )

    result = use_case.execute(
        ListWorkOrderActivitiesQuery(
            work_order_code="WO-001"
        )
    )

    assert result.items == []


def test_should_include_active_hold():

    (
        activity_repository,
        person_repository,
        hold_repository,
        use_case,
    ) = build_use_case()

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
        )
    )

    activity = create_activity(
        "ACT-001",
        "55464",
    )

    activity_repository.save(
        activity
    )

    hold = ActivityHold(
        code="AH-001",
        activity_code="ACT-001",
        reason=ActivityHoldReason.PENDING_MATERIAL,
        observations="Esperando material",
        held_at=datetime(
            2026,
            9,
            14,
            10,
            30,
        ),
        held_by_person_code="55464",
    )

    hold_repository.save(
        hold
    )

    result = use_case.execute(
        ListWorkOrderActivitiesQuery(
            work_order_code="WO-001"
        )
    )

    item = result.items[0]

    assert item.active_hold is not None
    assert item.active_hold.code == "AH-001"

    assert (
        item.active_hold.reason
        == ActivityHoldReason.PENDING_MATERIAL
    )

    assert (
        item.active_hold.observations
        == "Esperando material"
    )

    assert (
        item.active_hold.held_by_person_code
        == "55464"
    )

    assert item.held_by_person is not None

    assert (
        item.held_by_person.code
        == "55464"
    )

    assert (
        item.held_by_person.name
        == "Fortunato"
    )


def test_should_not_include_resumed_hold_as_active():

    (
        activity_repository,
        person_repository,
        hold_repository,
        use_case,
    ) = build_use_case()

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
        )
    )

    activity_repository.save(
        create_activity(
            "ACT-001",
            "55464",
        )
    )

    hold = ActivityHold(
        code="AH-001",
        activity_code="ACT-001",
        reason=ActivityHoldReason.PENDING_MATERIAL,
        observations="Esperando material",
        held_at=datetime(
            2026,
            9,
            14,
            10,
            30,
        ),
        held_by_person_code="55464",
        resumed_at=datetime(
            2026,
            9,
            14,
            11,
            0,
        ),
        resumed_by_person_code="55464",
    )

    hold_repository.save(
        hold
    )

    result = use_case.execute(
        ListWorkOrderActivitiesQuery(
            work_order_code="WO-001"
        )
    )

    assert (
        result.items[0].active_hold
        is None
    )


def test_should_keep_activity_when_hold_person_is_missing():

    (
        activity_repository,
        person_repository,
        hold_repository,
        use_case,
    ) = build_use_case()

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
        )
    )

    activity_repository.save(
        create_activity(
            "ACT-001",
            "55464",
        )
    )

    hold_repository.save(
        ActivityHold(
            code="AH-001",
            activity_code="ACT-001",
            reason=ActivityHoldReason.PENDING_MATERIAL,
            observations="Esperando material",
            held_at=datetime(
                2026,
                9,
                14,
                10,
                30,
            ),
            held_by_person_code="99999",
        )
    )

    result = use_case.execute(
        ListWorkOrderActivitiesQuery(
            work_order_code="WO-001"
        )
    )

    assert len(result.items) == 1

    item = result.items[0]

    assert item.active_hold is not None
    assert item.held_by_person is None


def test_should_include_activity_hold_history():

    (
        activity_repository,
        person_repository,
        hold_repository,
        use_case,
    ) = build_use_case()

    person_repository.save(
        Person(
            code="TECH-001",
            name="Técnico Uno",
        )
    )

    person_repository.save(
        Person(
            code="TECH-002",
            name="Técnico Dos",
        )
    )

    activity_repository.save(
        create_activity(
            "ACT-001",
            "TECH-001",
        )
    )

    hold_repository.save(
        ActivityHold(
            code="AH-001",
            activity_code="ACT-001",
            reason=(
                ActivityHoldReason.PENDING_MATERIAL
            ),
            observations="Esperando material",
            held_at=datetime(
                2026,
                9,
                14,
                10,
                0,
            ),
            held_by_person_code="TECH-001",
            resumed_at=datetime(
                2026,
                9,
                14,
                10,
                30,
            ),
            resumed_by_person_code="TECH-002",
        )
    )

    hold_repository.save(
        ActivityHold(
            code="AH-002",
            activity_code="ACT-001",
            reason=(
                ActivityHoldReason.EQUIPMENT_IN_USE
            ),
            observations="Área sin liberar",
            held_at=datetime(
                2026,
                9,
                14,
                11,
                0,
            ),
            held_by_person_code="TECH-002",
        )
    )

    result = use_case.execute(
        ListWorkOrderActivitiesQuery(
            work_order_code="WO-001"
        )
    )

    item = result.items[0]

    assert len(item.hold_history) == 2

    first = item.hold_history[0]
    second = item.hold_history[1]

    assert first.hold.code == "AH-001"

    assert first.held_by_person is not None
    assert first.held_by_person.name == "Técnico Uno"

    assert first.resumed_by_person is not None
    assert first.resumed_by_person.name == "Técnico Dos"

    assert second.hold.code == "AH-002"

    assert second.held_by_person is not None
    assert second.held_by_person.name == "Técnico Dos"

    assert second.resumed_by_person is None
