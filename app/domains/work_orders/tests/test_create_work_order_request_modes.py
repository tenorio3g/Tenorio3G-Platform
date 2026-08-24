from datetime import datetime
from unittest.mock import Mock

from app.domains.assets.repositories import (
    AssetRepository,
)

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.use_cases import (
    CreateWorkOrder,
    CreateWorkOrderCommand,
)

from app.foundation.timeline.engine.repositories import (
    InMemoryTimelineEventRepository,
)

from app.foundation.timeline.engine.use_cases import (
    RecordTimelineEvent,
)


def build_use_case(
    with_timeline=False,
):

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    asset_repository = Mock(
        spec=AssetRepository
    )

    person_repository = Mock(
        spec=PersonRepository
    )

    timeline_repository = None
    record_timeline_event = None

    if with_timeline:

        timeline_repository = (
            InMemoryTimelineEventRepository()
        )

        record_timeline_event = (
            RecordTimelineEvent(
                timeline_repository
            )
        )

    use_case = CreateWorkOrder(
        work_order_repository,
        asset_repository,
        person_repository,
        record_timeline_event,
    )

    return (
        work_order_repository,
        asset_repository,
        person_repository,
        timeline_repository,
        use_case,
    )


def base_command(
    **overrides,
):

    data = {
        "code": "WO-REQUEST-001",
        "title": "Instalar contacto 110 V",
        "description": (
            "Instalar contacto y punto "
            "de aire comprimido."
        ),
        "work_type": "PROJECT",
        "priority": "MEDIUM",
        "asset_code": "ASSET-001",
        "requester_person_code": "REQ-001",
        "supervisor_person_code": "SUP-001",
        "requester_name": None,
        "requester_phone": None,
        "requester_area": None,
        "location_description": None,
        "created_at": datetime(
            2026,
            8,
            22,
            21,
            0,
        ),
    }

    data.update(
        overrides
    )

    return CreateWorkOrderCommand(
        **data
    )


def configure_registered_people(
    person_repository,
):

    requester = Person(
        code="REQ-001",
        name="Solicitante Registrado",
    )

    supervisor = Person(
        code="SUP-001",
        name="Supervisor",
    )

    person_repository.get_by_code.side_effect = (
        lambda code: {
            "REQ-001": requester,
            "SUP-001": supervisor,
        }.get(code)
    )

    return (
        requester,
        supervisor,
    )


def test_should_create_without_asset():

    (
        repository,
        asset_repository,
        person_repository,
        _,
        use_case,
    ) = build_use_case()

    configure_registered_people(
        person_repository
    )

    result = use_case.execute(
        base_command(
            asset_code=None,
        )
    )

    assert (
        result.work_order.asset_code
        is None
    )

    asset_repository.find_by_code.assert_not_called()

    assert (
        repository.get_by_code(
            "WO-REQUEST-001"
        )
        is not None
    )


def test_should_create_without_supervisor():

    (
        _,
        asset_repository,
        person_repository,
        _,
        use_case,
    ) = build_use_case()

    asset_repository.find_by_code.return_value = (
        object()
    )

    requester = Person(
        code="REQ-001",
        name="Solicitante Registrado",
    )

    person_repository.get_by_code.return_value = (
        requester
    )

    result = use_case.execute(
        base_command(
            supervisor_person_code=None,
        )
    )

    assert (
        result.work_order.supervisor_person_code
        is None
    )


def test_should_create_with_manual_requester():

    (
        _,
        asset_repository,
        person_repository,
        _,
        use_case,
    ) = build_use_case()

    asset_repository.find_by_code.return_value = (
        object()
    )

    supervisor = Person(
        code="SUP-001",
        name="Supervisor",
    )

    person_repository.get_by_code.side_effect = (
        lambda code: {
            "SUP-001": supervisor,
        }.get(code)
    )

    result = use_case.execute(
        base_command(
            requester_person_code=None,
            requester_name="Juan Perez",
            requester_phone="1234",
            requester_area="Produccion MD2",
            location_description="Linea 4",
        )
    )

    work_order = result.work_order

    assert (
        work_order.requester_person_code
        is None
    )

    assert (
        work_order.requester_name
        == "Juan Perez"
    )

    assert (
        work_order.requester_phone
        == "1234"
    )

    assert (
        work_order.requester_area
        == "Produccion MD2"
    )

    assert (
        work_order.location_description
        == "Linea 4"
    )


def test_should_validate_asset_when_provided():

    (
        _,
        asset_repository,
        person_repository,
        _,
        use_case,
    ) = build_use_case()

    configure_registered_people(
        person_repository
    )

    asset_repository.find_by_code.return_value = (
        None
    )

    try:
        use_case.execute(
            base_command()
        )

        assert False, (
            "Expected ValueError"
        )

    except ValueError as error:

        assert str(error) == (
            "asset not found"
        )


def test_should_validate_registered_requester_when_provided():

    (
        _,
        asset_repository,
        person_repository,
        _,
        use_case,
    ) = build_use_case()

    asset_repository.find_by_code.return_value = (
        object()
    )

    person_repository.get_by_code.return_value = (
        None
    )

    try:
        use_case.execute(
            base_command()
        )

        assert False, (
            "Expected ValueError"
        )

    except ValueError as error:

        assert str(error) == (
            "requester not found"
        )


def test_should_validate_supervisor_when_provided():

    (
        _,
        asset_repository,
        person_repository,
        _,
        use_case,
    ) = build_use_case()

    asset_repository.find_by_code.return_value = (
        object()
    )

    requester = Person(
        code="REQ-001",
        name="Solicitante",
    )

    person_repository.get_by_code.side_effect = [
        requester,
        None,
    ]

    try:
        use_case.execute(
            base_command()
        )

        assert False, (
            "Expected ValueError"
        )

    except ValueError as error:

        assert str(error) == (
            "supervisor not found"
        )


def test_should_record_registered_requester_in_timeline():

    (
        _,
        asset_repository,
        person_repository,
        timeline_repository,
        use_case,
    ) = build_use_case(
        with_timeline=True
    )

    asset_repository.find_by_code.return_value = (
        object()
    )

    requester, _ = (
        configure_registered_people(
            person_repository
        )
    )

    result = use_case.execute(
        base_command()
    )

    events = (
        timeline_repository
        .list_by_entity(
            "WORK_ORDER",
            result.work_order.code,
        )
    )

    assert len(events) == 1

    event = events[0]

    assert (
        event.actor_person_code
        == requester.code
    )

    assert (
        event.actor_name
        == requester.name
    )


def test_should_record_manual_requester_in_timeline():

    (
        _,
        asset_repository,
        person_repository,
        timeline_repository,
        use_case,
    ) = build_use_case(
        with_timeline=True
    )

    asset_repository.find_by_code.return_value = (
        object()
    )

    supervisor = Person(
        code="SUP-001",
        name="Supervisor",
    )

    person_repository.get_by_code.side_effect = (
        lambda code: {
            "SUP-001": supervisor,
        }.get(code)
    )

    result = use_case.execute(
        base_command(
            requester_person_code=None,
            requester_name="Juan Perez",
            requester_phone="1234",
        )
    )

    events = (
        timeline_repository
        .list_by_entity(
            "WORK_ORDER",
            result.work_order.code,
        )
    )

    assert len(events) == 1

    event = events[0]

    assert (
        event.actor_person_code
        is None
    )

    assert (
        event.actor_name
        == "Juan Perez"
    )
