from sqlalchemy import select

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from app.domains.work_orders.technicians.models import (
    WorkOrderTechnicianAssignmentModel,
)

from .work_order_technician_assignment_repository import (
    WorkOrderTechnicianAssignmentRepository,
)


class SQLiteWorkOrderTechnicianAssignmentRepository(
    WorkOrderTechnicianAssignmentRepository,
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
        assignment: WorkOrderTechnicianAssignment,
    ) -> None:

        with self._session_factory() as session:

            key = (
                assignment.work_order_code,
                assignment.person_code,
            )

            existing = session.get(
                WorkOrderTechnicianAssignmentModel,
                key,
            )

            if existing is not None:
                raise ValueError(
                    "technician already assigned to work order"
                )

            model = (
                WorkOrderTechnicianAssignmentModel(
                    work_order_code=(
                        assignment.work_order_code
                    ),
                    person_code=(
                        assignment.person_code
                    ),
                    assigned_at=(
                        assignment.assigned_at
                    ),
                )
            )

            session.add(
                model
            )

            session.commit()

    def exists(
        self,
        work_order_code: str,
        person_code: str,
    ) -> bool:

        normalized_work_order_code = str(
            work_order_code
        ).strip().upper()

        normalized_person_code = str(
            person_code
        ).strip()

        with self._session_factory() as session:

            key = (
                normalized_work_order_code,
                normalized_person_code,
            )

            model = session.get(
                WorkOrderTechnicianAssignmentModel,
                key,
            )

            return model is not None

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderTechnicianAssignment]:

        normalized_work_order_code = str(
            work_order_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    WorkOrderTechnicianAssignmentModel
                )
                .where(
                    WorkOrderTechnicianAssignmentModel.work_order_code
                    == normalized_work_order_code
                )
                .order_by(
                    WorkOrderTechnicianAssignmentModel.assigned_at
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
        work_order_code: str,
        person_code: str,
    ) -> None:

        normalized_work_order_code = str(
            work_order_code
        ).strip().upper()

        normalized_person_code = str(
            person_code
        ).strip()

        with self._session_factory() as session:

            key = (
                normalized_work_order_code,
                normalized_person_code,
            )

            model = session.get(
                WorkOrderTechnicianAssignmentModel,
                key,
            )

            if model is not None:

                session.delete(
                    model
                )

                session.commit()

    @staticmethod
    def _to_entity(
        model: WorkOrderTechnicianAssignmentModel,
    ) -> WorkOrderTechnicianAssignment:

        return WorkOrderTechnicianAssignment(
            work_order_code=(
                model.work_order_code
            ),
            person_code=(
                model.person_code
            ),
            assigned_at=(
                model.assigned_at
            ),
        )