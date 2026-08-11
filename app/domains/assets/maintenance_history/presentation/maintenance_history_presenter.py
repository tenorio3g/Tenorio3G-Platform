from datetime import datetime

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from .maintenance_history_view_model import (
    MaintenanceEventItemViewModel,
    MaintenanceHistoryViewModel,
)


class MaintenanceHistoryPresenter:

    @staticmethod
    def present(
        events: list[MaintenanceEvent],
    ) -> MaintenanceHistoryViewModel:

        ordered_events = sorted(
            events,
            key=lambda event: (
                event.started_at
                if event.started_at is not None
                else datetime.min
            ),
            reverse=True,
        )

        items = [
            MaintenanceEventItemViewModel(
                code=event.code,
                event_type=event.event_type,
                title=event.title,
                description=event.description,
                performed_by=event.performed_by,
                started_at=event.started_at.strftime(
                    "%d/%m/%Y %H:%M"
                ),
                completed_at=(
                    event.completed_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                    if event.completed_at
                    else ""
                ),
                observations=event.observations,
                status=(
                    "Completado"
                    if event.is_completed
                    else "Abierto"
                ),
            )
            for event in ordered_events
        ]

        return MaintenanceHistoryViewModel(
            items=items
        )