from sqlalchemy import select

from app.domains.work_orders.materials.entities import (
    WorkOrderSparePartUsage,
)

from app.domains.work_orders.materials.models import (
    WorkOrderSparePartUsageModel,
)

from .work_order_spare_part_usage_repository import (
    WorkOrderSparePartUsageRepository,
)


class SQLiteWorkOrderSparePartUsageRepository(
    WorkOrderSparePartUsageRepository,
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
        usage: WorkOrderSparePartUsage,
    ) -> None:

        with self._session_factory() as session:

            model = WorkOrderSparePartUsageModel(
                work_order_code=(
                    usage.work_order_code
                ),
                spare_part_code=(
                    usage.spare_part_code
                ),
                quantity=usage.quantity,
                unit_cost=usage.unit_cost,
                used_at=usage.used_at,
                observations=(
                    usage.observations
                ),
            )

            session.add(
                model
            )

            session.commit()

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderSparePartUsage]:

        normalized_code = str(
            work_order_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    WorkOrderSparePartUsageModel
                )
                .where(
                    WorkOrderSparePartUsageModel.work_order_code
                    == normalized_code
                )
                .order_by(
                    WorkOrderSparePartUsageModel.used_at
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

    @staticmethod
    def _to_entity(
        model: WorkOrderSparePartUsageModel,
    ) -> WorkOrderSparePartUsage:

        return WorkOrderSparePartUsage(
            work_order_code=(
                model.work_order_code
            ),
            spare_part_code=(
                model.spare_part_code
            ),
            quantity=model.quantity,
            unit_cost=model.unit_cost,
            used_at=model.used_at,
            observations=(
                model.observations
            ),
        )