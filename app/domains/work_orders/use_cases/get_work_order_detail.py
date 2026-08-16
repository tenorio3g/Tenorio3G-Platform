from dataclasses import dataclass

from app.domains.assets.entities import (
    Asset,
)

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

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class GetWorkOrderDetailQuery:
    code: str


@dataclass(frozen=True)
class GetWorkOrderDetailResult:
    work_order: WorkOrder
    asset: Asset
    requester: Person
    supervisor: Person


class GetWorkOrderDetail:

    def __init__(
        self,
        work_order_repository: WorkOrderRepository,
        asset_repository: AssetRepository,
        person_repository: PersonRepository,
    ):
        self._work_order_repository = (
            work_order_repository
        )
        self._asset_repository = (
            asset_repository
        )
        self._person_repository = (
            person_repository
        )

    def execute(
        self,
        query: GetWorkOrderDetailQuery,
    ) -> GetWorkOrderDetailResult:

        work_order = (
            self._work_order_repository.get_by_code(
                query.code
            )
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        asset = self._asset_repository.find_by_code(
            work_order.asset_code
        )

        if asset is None:
            raise ValueError(
                "work order asset not found"
            )

        requester = (
            self._person_repository.get_by_code(
                work_order.requester_person_code
            )
        )

        if requester is None:
            raise ValueError(
                "work order requester not found"
            )

        supervisor = (
            self._person_repository.get_by_code(
                work_order.supervisor_person_code
            )
        )

        if supervisor is None:
            raise ValueError(
                "work order supervisor not found"
            )

        return GetWorkOrderDetailResult(
            work_order=work_order,
            asset=asset,
            requester=requester,
            supervisor=supervisor,
        )