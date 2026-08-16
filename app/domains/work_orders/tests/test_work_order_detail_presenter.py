from datetime import date, datetime

from app.domains.assets.entities import (
    Asset,
)

from app.domains.assets.value_objects import (
    AssetStatus,
)

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.presentation import (
    WorkOrderDetailPresenter,
    WorkOrderDetailViewModel,
)


def test_should_present_work_order_detail():

    work_order = WorkOrder(
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
            16,
            8,
            30,
        ),
    )

    asset = Asset(
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

    requester = Person(
        code="55464",
        name="Fortunato",
        position="Técnico",
    )

    supervisor = Person(
        code="12",
        name="Pedro",
        position="Supervisor",
    )

    result = WorkOrderDetailPresenter.present(
        work_order,
        asset,
        requester,
        supervisor,
    )

    assert isinstance(
        result,
        WorkOrderDetailViewModel,
    )

    assert result.code == "WO-001"
    assert result.status == "CREATED"

    assert (
        result.asset.code
        == "S2-480-ES09-T269"
    )

    assert (
        result.asset.name
        == "TABLERO GENERAL ES09"
    )

    assert (
        result.asset.location_code
        == "SUBESTACION-ES09"
    )

    assert result.requester.code == "55464"
    assert result.requester.name == "Fortunato"

    assert result.supervisor.code == "12"
    assert result.supervisor.name == "Pedro"

    assert (
        result.created_at
        == "16/08/2026 08:30"
    )