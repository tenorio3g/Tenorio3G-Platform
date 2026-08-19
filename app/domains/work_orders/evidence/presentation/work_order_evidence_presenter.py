from app.domains.work_orders.evidence.use_cases import (
    ListWorkOrderEvidenceResult,
)

from .work_order_evidence_view_model import (
    WorkOrderEvidenceItemViewModel,
    WorkOrderEvidenceViewModel,
)


class WorkOrderEvidencePresenter:

    TYPE_LABELS = {
        "BEFORE_PHOTO": "Foto antes",
        "AFTER_PHOTO": "Foto después",
        "MEASUREMENT": "Medición",
        "DOCUMENT": "Documento",
        "OTHER": "Otro",
    }

    @classmethod
    def present(
        cls,
        result: ListWorkOrderEvidenceResult,
    ) -> WorkOrderEvidenceViewModel:

        items = []

        for item in result.items:

            file_name_lower = (
                item.file_name.lower()
            )

            is_image = (
                file_name_lower.endswith(".jpg")
                or file_name_lower.endswith(".jpeg")
                or file_name_lower.endswith(".png")
            )

            is_pdf = (
                file_name_lower.endswith(".pdf")
            )

            items.append(
                WorkOrderEvidenceItemViewModel(
                    evidence_id=item.evidence_id,
                    title=item.title,
                    evidence_type=(
                        item.evidence_type.value
                    ),
                    evidence_type_label=(
                        cls.TYPE_LABELS.get(
                            item.evidence_type.value,
                            item.evidence_type.value,
                        )
                    ),
                    file_name=item.file_name,
                    registered_by_person_code=(
                        item.registered_by_person_code
                    ),
                    created_at=(
                        item.created_at.strftime(
                            "%d/%m/%Y %H:%M"
                        )
                    ),
                    description=item.description,
                    activity_code=item.activity_code,
                    is_image=is_image,
                    is_pdf=is_pdf,
                )
            )

        return WorkOrderEvidenceViewModel(
            items=items
        )