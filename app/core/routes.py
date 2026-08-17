from flask import (
    Blueprint,
    render_template,
)

from app.core.dashboard import (
    DashboardService,
)

from app.domains.assets.bootstrap.assets_container import (
    repository as asset_repository,
)

from app.domains.identity.people.bootstrap import (
    person_repository,
)

from app.domains.work_orders.bootstrap import (
    work_order_repository,
)

from app.domains.work_orders.activities.bootstrap import (
    work_order_activity_repository,
)


core = Blueprint(
    "core",
    __name__,
)


@core.route("/")
def dashboard():

    service = DashboardService(
        asset_repository=asset_repository,
        work_order_repository=(
            work_order_repository
        ),
        person_repository=(
            person_repository
        ),
        activity_repository=(
            work_order_activity_repository
        ),
    )

    dashboard_vm = service.build()

    return render_template(
        "pages/dashboard.html",
        dashboard=dashboard_vm,
    )