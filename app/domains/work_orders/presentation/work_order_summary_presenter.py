from app.domains.work_orders.use_cases.list_work_order_summaries import (
    ListWorkOrderSummariesResult,
)

from .work_order_summary_view_model import (
    WorkOrderSummaryItemViewModel,
    WorkOrderSummaryViewModel,
)


class WorkOrderSummaryPresenter:

    STATUS_LABELS = {
        "CREATED": "Creada",
        "ASSIGNED": "Asignada",
        "IN_PROGRESS": "En proceso",
        "ON_HOLD": "En pausa",
        "COMPLETED": "Completada",
        "CLOSED": "Cerrada",
        "CANCELLED": "Cancelada",
    }

    OPERATIONAL_STATE_LABELS = {
        "ACTIVE": "Activa",
        "FINISHED": "Finalizada",
        "CANCELLED": "Cancelada",
    }

    ACTIVE_STATUSES = {
        "CREATED",
        "ASSIGNED",
        "IN_PROGRESS",
        "ON_HOLD",
    }

    FINISHED_STATUSES = {
        "COMPLETED",
        "CLOSED",
    }

    @classmethod
    def present(
        cls,
        result: ListWorkOrderSummariesResult,
    ) -> WorkOrderSummaryViewModel:

        items = []

        for summary in result.items:

            work_order = summary.work_order

            status = (
                work_order.status.value
            )

            operational_state = (
                cls._get_operational_state(
                    status
                )
            )

            if status in (
                "COMPLETED",
                "CLOSED",
                "CANCELLED",
            ):
                technician_label = (
                    "Participaron"
                )

                technicians = (
                    summary.participant_technicians
                )

            else:
                technician_label = (
                    "Realizando"
                )

                technicians = (
                    summary.active_technicians
                )

            items.append(
                WorkOrderSummaryItemViewModel(
                    code=work_order.code,
                    title=work_order.title,

                    status=status,
                    status_label=(
                        cls.STATUS_LABELS.get(
                            status,
                            status,
                        )
                    ),

                    operational_state=(
                        operational_state
                    ),
                    operational_state_label=(
                        cls.OPERATIONAL_STATE_LABELS[
                            operational_state
                        ]
                    ),

                    priority=(
                        work_order.priority
                    ),
                    work_type=(
                        work_order.work_type
                    ),

                    asset_code=(
                        work_order.asset_code
                    ),
                    asset_name=(
                        summary.asset.name
                        if summary.asset
                        else "Activo no disponible"
                    ),

                    requester_code=(
                        work_order.requester_person_code
                    ),
                    requester_name=(
                        summary.requester.name
                        if summary.requester
                        else "Solicitante no disponible"
                    ),

                    supervisor_code=(
                        work_order.supervisor_person_code
                    ),
                    supervisor_name=(
                        summary.supervisor.name
                        if summary.supervisor
                        else "Supervisor no disponible"
                    ),

                    technician_label=(
                        technician_label
                    ),
                    technician_names=[
                        person.name
                        for person in technicians
                    ],

                    created_at=(
                        work_order.created_at.strftime(
                            "%d/%m/%Y %H:%M"
                        )
                    ),
                )
            )

        return WorkOrderSummaryViewModel(
            items=items
        )

    @classmethod
    def _get_operational_state(
        cls,
        status: str,
    ) -> str:

        if status in cls.ACTIVE_STATUSES:
            return "ACTIVE"

        if status in cls.FINISHED_STATUSES:
            return "FINISHED"

        return "CANCELLED"
