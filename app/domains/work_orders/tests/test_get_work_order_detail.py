from datetime import date, datetime

import pytest

from app.domains.assets.entities import (
    Asset,
)

from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
)

from app.domains.assets.value_objects import (
    AssetStatus,
)

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.use_cases import (
    GetWorkOrderDetail,
    GetWorkOrderDetailQuery,
)


def create_asset():

    return Asset(
        code="S2-480-ES09-T269",
        name="TABLERO GENERAL ES09",
        asset_model_code="MODEL-001",
        serial_number="SERIAL-001",
        location_code="SUBESTACION-ES09",
        status=AssetStatus.OPERATING,
        installation_date=date(
            2026,
            1,
            1,
        ),
    )


def create_work_order():

    return WorkOrder(
        code="WO-001",
        title="Inspección general",
        description="Revisión del tablero.",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code="S2-480-ES09-T269",
        requester_person_code="55464",
        supervisor_person_code="12",
        created_at=datetime(
            2026,
            8,
            15,
            8,
            0,
        ),
    )


def build_use_case():

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    asset_repository = (
        InMemoryAssetRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    use_case = GetWorkOrderDetail(
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


def configure_valid_data(
    work_order_repository,
    asset_repository,
    person_repository,
):

    work_order_repository.save(
        create_work_order()
    )

    asset_repository.save(
        create_asset()
    )

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
            position="Técnico",
        )
    )

    person_repository.save(
        Person(
            code="12",
            name="Pedro",
            position="Supervisor",
        )
    )


def test_should_get_complete_work_order_detail():

    (
        work_order_repository,
        asset_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    configure_valid_data(
        work_order_repository,
        asset_repository,
        person_repository,
    )

    result = use_case.execute(
        GetWorkOrderDetailQuery(
            code=" wo-001 "
        )
    )

    assert result.work_order.code == "WO-001"

    assert (
        result.asset.code
        == "S2-480-ES09-T269"
    )

    assert (
        result.requester.code
        == "55464"
    )

    assert (
        result.supervisor.code
        == "12"
    )


def test_should_reject_unknown_work_order():

    (
        _,
        _,
        _,
        use_case,
    ) = build_use_case()

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            GetWorkOrderDetailQuery(
                code="WO-404"
            )
        )


def test_should_reject_missing_asset():

    (
        work_order_repository,
        _,
        person_repository,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

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

    with pytest.raises(
        ValueError,
        match="work order asset not found",
    ):
        use_case.execute(
            GetWorkOrderDetailQuery(
                code="WO-001"
            )
        )


def test_should_reject_missing_requester():

    (
        work_order_repository,
        asset_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    asset_repository.save(
        create_asset()
    )

    person_repository.save(
        Person(
            code="12",
            name="Pedro",
        )
    )

    with pytest.raises(
        ValueError,
        match="work order requester not found",
    ):
        use_case.execute(
            GetWorkOrderDetailQuery(
                code="WO-001"
            )
        )


def test_should_reject_missing_supervisor():

    (
        work_order_repository,
        asset_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    asset_repository.save(
        create_asset()
    )

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
        )
    )

    with pytest.raises(
        ValueError,
        match="work order supervisor not found",
    ):
        use_case.execute(
            GetWorkOrderDetailQuery(
                code="WO-001"
            )
        )