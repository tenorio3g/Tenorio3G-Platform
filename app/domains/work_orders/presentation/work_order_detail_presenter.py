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
        asset: Asset | None,
        requester: Person | None,
        supervisor: Person | None,
    ) -> WorkOrderDetailViewModel:

        # ====================================================
        # ASSET
        # ====================================================

        if asset is not None:

            asset_view_model = (
                WorkOrderAssetViewModel(
                    code=asset.code,
                    name=asset.name,
                    location_code=(
                        asset.location_code
                    ),
                )
            )

        else:

            asset_view_model = (
                WorkOrderAssetViewModel(
                    code=None,
                    name="No aplica",
                    location_code=None,
                )
            )

        # ====================================================
        # REQUESTER
        # ====================================================

        if requester is not None:

            requester_view_model = (
                WorkOrderPersonViewModel(
                    code=requester.code,
                    name=requester.name,
                    position=(
                        requester.position
                        or "Sin puesto registrado"
                    ),
                    phone=(
                        work_order.requester_phone
                    ),
                    area=(
                        work_order.requester_area
                    ),
                )
            )

        else:

            requester_view_model = (
                WorkOrderPersonViewModel(
                    code=None,
                    name=(
                        work_order.requester_name
                        or "Solicitante no disponible"
                    ),
                    position=(
                        "Solicitante no registrado"
                    ),
                    phone=(
                        work_order.requester_phone
                    ),
                    area=(
                        work_order.requester_area
                    ),
                )
            )

        # ====================================================
        # SUPERVISOR
        # ====================================================

        if supervisor is not None:

            supervisor_view_model = (
                WorkOrderPersonViewModel(
                    code=supervisor.code,
                    name=supervisor.name,
                    position=(
                        supervisor.position
                        or "Sin puesto registrado"
                    ),
                )
            )

        else:

            supervisor_view_model = (
                WorkOrderPersonViewModel(
                    code=None,
                    name="Pendiente de revision",
                    position=(
                        "Sin supervisor asignado"
                    ),
                )
            )

        # ====================================================
        # WORK ORDER
        # ====================================================

        return WorkOrderDetailViewModel(
            code=work_order.code,
            title=work_order.title,
            description=(
                work_order.description
            ),
            work_type=(
                work_order.work_type
            ),
            priority=(
                work_order.priority
            ),
            status=(
                work_order.status.value
            ),
            created_at=(
                work_order.created_at.strftime(
                    "%d/%m/%Y %H:%M"
                )
            ),
            asset=asset_view_model,
            requester=(
                requester_view_model
            ),
            supervisor=(
                supervisor_view_model
            ),
            location_description=(
                work_order.location_description
            ),
        )
