from sqlalchemy import select

from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)

from app.domains.work_orders.evidence.models import (
    WorkOrderEvidenceModel,
)

from app.domains.work_orders.evidence.value_objects import (
    EvidenceType,
)

from .work_order_evidence_repository import (
    WorkOrderEvidenceRepository,
)


class SQLiteWorkOrderEvidenceRepository(
    WorkOrderEvidenceRepository,
):

    def __init__(
        self,
        session_factory,
    ):
        self._session_factory = session_factory

    def save(
        self,
        evidence: WorkOrderEvidence,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                WorkOrderEvidenceModel,
                evidence.evidence_id,
            )

            if model is None:

                model = WorkOrderEvidenceModel(
                    evidence_id=evidence.evidence_id,
                    work_order_code=evidence.work_order_code,
                    title=evidence.title,
                    evidence_type=evidence.evidence_type.value,
                    file_name=evidence.file_name,
                    registered_by_person_code=(
                        evidence.registered_by_person_code
                    ),
                    created_at=evidence.created_at,
                    description=evidence.description,
                    activity_code=evidence.activity_code,
                )

                session.add(model)

            else:

                model.work_order_code = (
                    evidence.work_order_code
                )

                model.title = evidence.title

                model.evidence_type = (
                    evidence.evidence_type.value
                )

                model.file_name = evidence.file_name

                model.registered_by_person_code = (
                    evidence.registered_by_person_code
                )

                model.created_at = evidence.created_at

                model.description = (
                    evidence.description
                )

                model.activity_code = (
                    evidence.activity_code
                )

            session.commit()

    def get_by_id(
        self,
        evidence_id: str,
    ) -> WorkOrderEvidence | None:

        normalized_id = str(
            evidence_id
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                WorkOrderEvidenceModel,
                normalized_id,
            )

            if model is None:
                return None

            return self._to_entity(model)

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderEvidence]:

        normalized_code = str(
            work_order_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    WorkOrderEvidenceModel
                )
                .where(
                    WorkOrderEvidenceModel.work_order_code
                    == normalized_code
                )
                .order_by(
                    WorkOrderEvidenceModel.created_at
                )
            )

            models = (
                session.execute(statement)
                .scalars()
                .all()
            )

            return [
                self._to_entity(model)
                for model in models
            ]

    def delete(
        self,
        evidence_id: str,
    ) -> None:

        normalized_id = str(
            evidence_id
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                WorkOrderEvidenceModel,
                normalized_id,
            )

            if model is not None:
                session.delete(model)
                session.commit()

    @staticmethod
    def _to_entity(
        model: WorkOrderEvidenceModel,
    ) -> WorkOrderEvidence:

        return WorkOrderEvidence(
            evidence_id=model.evidence_id,
            work_order_code=model.work_order_code,
            title=model.title,
            evidence_type=EvidenceType(
                model.evidence_type
            ),
            file_name=model.file_name,
            registered_by_person_code=(
                model.registered_by_person_code
            ),
            created_at=model.created_at,
            description=model.description,
            activity_code=model.activity_code,
        )