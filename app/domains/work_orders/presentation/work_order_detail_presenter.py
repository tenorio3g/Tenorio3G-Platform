from app.domains.assets.entities import (
    Asset,
)

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from .work_order_detail_view_model import (
    WorkOrderAssetViewModel,
    WorkOrderDetailViewModel,
    WorkOrderPersonViewModel,
)


class WorkOrderDetailPresenter:

    @staticmethod
    def present(
        work_order: WorkOrder,
        asset: Asset,
        requester: Person,
        supervisor: Person,
    ) -> WorkOrderDetailViewModel:

        return WorkOrderDetailViewModel(
            code=work_order.code,
            title=work_order.title,
            description=work_order.description,
            work_type=work_order.work_type,
            priority=work_order.priority,
            status=work_order.status.value,
            created_at=(
                work_order.created_at.strftime(
                    "%d/%m/%Y %H:%M"
                )
            ),
            asset=WorkOrderAssetViewModel(
                code=asset.code,
                name=asset.name,
                location_code=asset.location_code,
            ),
            requester=WorkOrderPersonViewModel(
                code=requester.code,
                name=requester.name,
                position=(
                    requester.position
                    or "Sin puesto registrado"
                ),
            ),
            supervisor=WorkOrderPersonViewModel(
                code=supervisor.code,
                name=supervisor.name,
                position=(
                    supervisor.position
                    or "Sin puesto registrado"
                ),
            ),
        )