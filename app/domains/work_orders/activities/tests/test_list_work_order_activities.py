from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
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

    use_case = ListWorkOrderActivities(
        activity_repository,
        person_repository,
    )

    return (
        activity_repository,
        person_repository,
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


def test_should_list_multiple_activities():

    (
        activity_repository,
        person_repository,
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

    _, _, use_case = build_use_case()

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