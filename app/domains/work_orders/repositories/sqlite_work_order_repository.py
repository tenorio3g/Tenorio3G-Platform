from sqlalchemy import select

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.models import (
    WorkOrderModel,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from .work_order_repository import (
    WorkOrderRepository,
)


class SQLiteWorkOrderRepository(
    WorkOrderRepository,
):

    def __init__(
        self,
        session_factory,
    ):
        self._session_factory = (
            session_factory
        )

    def save(
        self,
        work_order: WorkOrder,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                WorkOrderModel,
                work_order.code,
            )

            if model is None:

                model = WorkOrderModel(
                    code=work_order.code,
                    title=work_order.title,
                    description=work_order.description,
                    work_type=work_order.work_type,
                    priority=work_order.priority,
                    asset_code=(
                        work_order.asset_code
                    ),
                    requester_person_code=(
                        work_order.requester_person_code
                    ),
                    requester_name=(
                        work_order.requester_name
                    ),
                    requester_phone=(
                        work_order.requester_phone
                    ),
                    requester_area=(
                        work_order.requester_area
                    ),
                    supervisor_person_code=(
                        work_order.supervisor_person_code
                    ),
                    location_description=(
                        work_order.location_description
                    ),
                    status=(
                        work_order.status.value
                    ),
                    created_at=(
                        work_order.created_at
                    ),
                )

                session.add(
                    model
                )

            else:

                model.title = (
                    work_order.title
                )

                model.description = (
                    work_order.description
                )

                model.work_type = (
                    work_order.work_type
                )

                model.priority = (
                    work_order.priority
                )

                model.asset_code = (
                    work_order.asset_code
                )

                model.requester_person_code = (
                    work_order.requester_person_code
                )

                model.requester_name = (
                    work_order.requester_name
                )

                model.requester_phone = (
                    work_order.requester_phone
                )

                model.requester_area = (
                    work_order.requester_area
                )

                model.supervisor_person_code = (
                    work_order.supervisor_person_code
                )

                model.location_description = (
                    work_order.location_description
                )

                model.status = (
                    work_order.status.value
                )

                model.created_at = (
                    work_order.created_at
                )

            session.commit()

    def get_by_code(
        self,
        code: str,
    ) -> WorkOrder | None:

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                WorkOrderModel,
                normalized_code,
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )

    def list_all(
        self,
    ) -> list[WorkOrder]:

        with self._session_factory() as session:

            statement = select(
                WorkOrderModel
            )

            models = (
                session.execute(
                    statement
                )
                .scalars()
                .all()
            )

            return [
                self._to_entity(model)
                for model in models
            ]

    def list_by_asset(
        self,
        asset_code: str,
    ) -> list[WorkOrder]:

        normalized_asset_code = str(
            asset_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    WorkOrderModel
                )
                .where(
                    WorkOrderModel.asset_code
                    == normalized_asset_code
                )
            )

            models = (
                session.execute(
                    statement
                )
                .scalars()
                .all()
            )

            return [
                self._to_entity(model)
                for model in models
            ]

    def delete(
        self,
        code: str,
    ) -> None:

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                WorkOrderModel,
                normalized_code,
            )

            if model is not None:

                session.delete(
                    model
                )

                session.commit()

    @staticmethod
    def _to_entity(
        model: WorkOrderModel,
    ) -> WorkOrder:

        return WorkOrder(
            code=model.code,
            title=model.title,
            description=model.description,
            work_type=model.work_type,
            priority=model.priority,
            asset_code=model.asset_code,
            requester_person_code=(
                model.requester_person_code
            ),
            requester_name=(
                model.requester_name
            ),
            requester_phone=(
                model.requester_phone
            ),
            requester_area=(
                model.requester_area
            ),
            supervisor_person_code=(
                model.supervisor_person_code
            ),
            location_description=(
                model.location_description
            ),
            created_at=model.created_at,
            status=WorkOrderStatus(
                model.status
            ),
        )
