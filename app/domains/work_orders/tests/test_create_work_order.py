from datetime import datetime
from unittest.mock import Mock

import pytest

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

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


def build_use_case():

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    asset_repository = Mock(
        spec=AssetRepository
    )

    person_repository = Mock(
        spec=PersonRepository
    )

    use_case = CreateWorkOrder(
        work_order_repository,
        asset_repository,
        person_repository,
    )

    return (
        work_order_repository,
        asset_repository,
        person_repository,
        use_case,
    )


def create_command():

    return CreateWorkOrderCommand(
        code="wo-001",
        title="Inspección de tablero",
        description="Revisión general.",
        work_type="preventive",
        priority="high",
        asset_code="asset-001",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            8,
            15,
            18,
            0,
        ),
    )


def configure_valid_dependencies(
    asset_repository,
    person_repository,
):

    asset_repository.find_by_code.return_value = (
        object()
    )

    requester = Person(
        code="REQ-001",
        name="Solicitante",
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


def test_should_create_work_order():

    (
        work_order_repository,
        asset_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    configure_valid_dependencies(
        asset_repository,
        person_repository,
    )

    result = use_case.execute(
        create_command()
    )

    persisted = (
        work_order_repository
        .get_by_code(
            "WO-001"
        )
    )

    assert persisted is not None

    assert (
        result.work_order.code
        == "WO-001"
    )

    assert (
        result.work_order.status
        == WorkOrderStatus.CREATED
    )


def test_should_reject_duplicate_work_order():

    (
        work_order_repository,
        asset_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    configure_valid_dependencies(
        asset_repository,
        person_repository,
    )

    command = create_command()

    use_case.execute(
        command
    )

    with pytest.raises(
        ValueError,
        match="work order already exists",
    ):
        use_case.execute(
            command
        )


def test_should_reject_unknown_asset():

    (
        _,
        asset_repository,
        _,
        use_case,
    ) = build_use_case()

    asset_repository.find_by_code.return_value = (
        None
    )

    with pytest.raises(
        ValueError,
        match="asset not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_unknown_requester():

    (
        _,
        asset_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    asset_repository.find_by_code.return_value = (
        object()
    )

    person_repository.get_by_code.return_value = (
        None
    )

    with pytest.raises(
        ValueError,
        match="requester not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_inactive_requester():

    (
        _,
        asset_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    asset_repository.find_by_code.return_value = (
        object()
    )

    person_repository.get_by_code.return_value = (
        Person(
            code="REQ-001",
            name="Solicitante",
            is_active=False,
        )
    )

    with pytest.raises(
        ValueError,
        match="requester is inactive",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_unknown_supervisor():

    (
        _,
        asset_repository,
        person_repository,
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

    with pytest.raises(
        ValueError,
        match="supervisor not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_inactive_supervisor():

    (
        _,
        asset_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    asset_repository.find_by_code.return_value = (
        object()
    )

    requester = Person(
        code="REQ-001",
        name="Solicitante",
    )

    supervisor = Person(
        code="SUP-001",
        name="Supervisor",
        is_active=False,
    )

    person_repository.get_by_code.side_effect = [
        requester,
        supervisor,
    ]

    with pytest.raises(
        ValueError,
        match="supervisor is inactive",
    ):
        use_case.execute(
            create_command()
        )