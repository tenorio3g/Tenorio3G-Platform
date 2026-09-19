class DailyReportTextPresenter:

    @staticmethod
    def present(report) -> str:

        lines = [
            "*REPORTE DE ACTIVIDADES*",
            "*" + report.report_date.strftime("%d/%m/%Y") + "*",
        ]

        DailyReportTextPresenter._append_work_orders(
            lines=lines,
            work_orders=report.work_orders,
        )

        DailyReportTextPresenter._append_operational_activities(
            lines=lines,
            operational_activities=(
                report.operational_activities
            ),
        )

        return "\n".join(lines)

    @staticmethod
    def _append_work_orders(
        lines,
        work_orders,
    ) -> None:

        for work_order in work_orders:

            for activity in work_order.activities:

                lines.append("")

                schedule = (
                    DailyReportTextPresenter
                    ._format_work_order_schedule(
                        activity
                    )
                )

                lines.append(f"*{schedule}*")
                lines.append(activity.title)

                lines.append(
                    f"*OT:* {work_order.work_order_code}"
                )

                if activity.technicians:

                    technician_codes = [
                        technician.person_code
                        for technician
                        in activity.technicians
                    ]

                    lines.append(
                        "*Tecnicos:* "
                        + ", ".join(
                            technician_codes
                        )
                    )

                if activity.completion_notes:
                    lines.append(
                        "*Resultado:* "
                        f"{activity.completion_notes}"
                    )

    @staticmethod
    def _format_work_order_schedule(
        activity,
    ) -> str:

        if activity.first_started_at is None:
            started_at = "Sin inicio registrado"
        else:
            started_at = (
                activity.first_started_at
                .strftime("%H:%M")
            )

        if activity.has_active_session:
            ended_at = "En proceso"

        elif activity.last_ended_at is not None:
            ended_at = (
                activity.last_ended_at
                .strftime("%H:%M")
            )

        else:
            ended_at = "Sin termino registrado"

        return f"{started_at} - {ended_at}"

    @staticmethod
    def _append_operational_activities(
        lines,
        operational_activities,
    ) -> None:

        for activity in operational_activities:

            lines.append("")

            started_at = (
                activity.started_at.strftime("%H:%M")
            )

            if activity.ended_at is None:
                schedule = (
                    f"{started_at} - En proceso"
                )
            else:
                ended_at = (
                    activity.ended_at.strftime("%H:%M")
                )

                schedule = (
                    f"{started_at} - {ended_at}"
                )

            lines.append(f"*{schedule}*")
            lines.append(activity.description)

            if activity.area:
                lines.append(
                    f"*Area:* {activity.area}"
                )

            if activity.location_description:
                lines.append(
                    "*Ubicacion:* "
                    f"{activity.location_description}"
                )

            if activity.result_notes:
                lines.append(
                    "*Resultado:* "
                    f"{activity.result_notes}"
                )
