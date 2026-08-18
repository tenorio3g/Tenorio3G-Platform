from sqlalchemy import select

from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)

from app.domains.work_orders.tools.models import (
    WorkOrderToolUsageModel,
)

from app.domains.work_orders.tools.value_objects import (
    ToolUsageStatus,
)

from .work_order_tool_usage_repository import (
    WorkOrderToolUsageRepository,
)


class SQLiteWorkOrderToolUsageRepository(
    WorkOrderToolUsageRepository,
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
        usage: WorkOrderToolUsage,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                WorkOrderToolUsageModel,
                usage.usage_id,
            )

            if model is None:

                model = WorkOrderToolUsageModel(
                    usage_id=usage.usage_id,
                    work_order_code=usage.work_order_code,
                    tool_code=usage.tool_code,
                    tool_name=usage.tool_name,
                    quantity=usage.quantity,
                    issued_at=usage.issued_at,
                    returned_at=usage.returned_at,
                    status=usage.status.value,
                    observations=usage.observations,
                )

                session.add(
                    model
                )

            else:

                model.work_order_code = (
                    usage.work_order_code
                )

                model.tool_code = (
                    usage.tool_code
                )

                model.tool_name = (
                    usage.tool_name
                )

                model.quantity = (
                    usage.quantity
                )

                model.issued_at = (
                    usage.issued_at
                )

                model.returned_at = (
                    usage.returned_at
                )

                model.status = (
                    usage.status.value
                )

                model.observations = (
                    usage.observations
                )

            session.commit()

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderToolUsage]:

        normalized_code = str(
            work_order_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    WorkOrderToolUsageModel
                )
                .where(
                    WorkOrderToolUsageModel.work_order_code
                    == normalized_code
                )
                .order_by(
                    WorkOrderToolUsageModel.issued_at
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
        model: WorkOrderToolUsageModel,
    ) -> WorkOrderToolUsage:

        return WorkOrderToolUsage(
            usage_id=model.usage_id,
            work_order_code=model.work_order_code,
            tool_code=model.tool_code,
            tool_name=model.tool_name,
            quantity=model.quantity,
            issued_at=model.issued_at,
            observations=model.observations,
            status=ToolUsageStatus(
                model.status
            ),
            returned_at=model.returned_at,
        )

    def get_by_id(
        self,
        usage_id: str,
    ) -> WorkOrderToolUsage | None:

        normalized_id = str(
            usage_id
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                WorkOrderToolUsageModel,
                normalized_id,
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )