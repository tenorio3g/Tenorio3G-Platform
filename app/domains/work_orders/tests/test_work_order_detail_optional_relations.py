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

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.presentation import (
    WorkOrderDetailPresenter,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.use_cases import (
    GetWorkOrderDetail,
    GetWorkOrderDetailQuery,
)


def build_use_case(
    work_order,
):

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    work_order_repository.save(
        work_order
    )

    asset_repository = Mock(
        spec=AssetRepository
    )

    person_repository = Mock(
        spec=PersonRepository
    )

    use_case = GetWorkOrderDetail(
        work_order_repository,
        asset_repository,
        person_repository,
    )

    return (
        asset_repository,
        person_repository,
        use_case,
    )


def create_work_order(
    *,
    asset_code=None,
    requester_person_code=None,
    supervisor_person_code=None,
    requester_name="Juan Perez",
    requester_phone="1234",
    requester_area="Produccion MD2",
    location_description="Linea 4",
):

    return WorkOrder(
        code="WO-DETAIL-001",
        title="Instalar contacto 110 V",
        description=(
            "Instalar contacto y aire comprimido."
        ),
        work_type="PROJECT",
        priority="MEDIUM",
        asset_code=asset_code,
        requester_person_code=(
            requester_person_code
        ),
        supervisor_person_code=(
            supervisor_person_code
        ),
        requester_name=requester_name,
        requester_phone=requester_phone,
        requester_area=requester_area,
        location_description=(
            location_description
        ),
        created_at=datetime(
            2026,
            8,
            22,
            12,
            0,
        ),
    )


def test_should_get_detail_without_asset():

    work_order = create_work_order()

    (
        asset_repository,
        _,
        use_case,
    ) = build_use_case(
        work_order
    )

    result = use_case.execute(
        GetWorkOrderDetailQuery(
            code="WO-DETAIL-001"
        )
    )

    assert result.asset is None

    asset_repository.find_by_code.assert_not_called()


def test_should_get_detail_without_supervisor():

    work_order = create_work_order()

    (
        _,
        person_repository,
        use_case,
    ) = build_use_case(
        work_order
    )

    result = use_case.execute(
        GetWorkOrderDetailQuery(
            code="WO-DETAIL-001"
        )
    )

    assert result.supervisor is None

    person_repository.get_by_code.assert_not_called()


def test_should_get_manual_requester_detail():

    work_order = create_work_order()

    (
        _,
        _,
        use_case,
    ) = build_use_case(
        work_order
    )

    result = use_case.execute(
        GetWorkOrderDetailQuery(
            code="WO-DETAIL-001"
        )
    )

    assert result.requester is None

    view_model = (
        WorkOrderDetailPresenter.present(
            result.work_order,
            result.asset,
            result.requester,
            result.supervisor,
        )
    )

    assert (
        view_model.requester.name
        == "Juan Perez"
    )

    assert (
        view_model.requester.phone
        == "1234"
    )

    assert (
        view_model.requester.area
        == "Produccion MD2"
    )


def test_should_present_missing_asset():

    work_order = create_work_order()

    (
        _,
        _,
        use_case,
    ) = build_use_case(
        work_order
    )

    result = use_case.execute(
        GetWorkOrderDetailQuery(
            code="WO-DETAIL-001"
        )
    )

    view_model = (
        WorkOrderDetailPresenter.present(
            result.work_order,
            result.asset,
            result.requester,
            result.supervisor,
        )
    )

    assert view_model.asset.code is None

    assert (
        view_model.asset.name
        == "No aplica"
    )

    assert (
        view_model.location_description
        == "Linea 4"
    )


def test_should_present_pending_supervisor():

    work_order = create_work_order()

    (
        _,
        _,
        use_case,
    ) = build_use_case(
        work_order
    )

    result = use_case.execute(
        GetWorkOrderDetailQuery(
            code="WO-DETAIL-001"
        )
    )

    view_model = (
        WorkOrderDetailPresenter.present(
            result.work_order,
            result.asset,
            result.requester,
            result.supervisor,
        )
    )

    assert (
        view_model.supervisor.name
        == "Pendiente de revision"
    )


def test_should_use_registered_requester():

    work_order = create_work_order(
        requester_person_code="REQ-001",
        requester_name=None,
        requester_phone=None,
        requester_area=None,
    )

    (
        _,
        person_repository,
        use_case,
    ) = build_use_case(
        work_order
    )

    requester = Person(
        code="REQ-001",
        name="Solicitante Registrado",
    )

    person_repository.get_by_code.return_value = (
        requester
    )

    result = use_case.execute(
        GetWorkOrderDetailQuery(
            code="WO-DETAIL-001"
        )
    )

    assert result.requester is requester
