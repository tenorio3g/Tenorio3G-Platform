from app.operations.daily_reports.queries import (
    GetDailyOperationalReport,
)

from app.operations.daily_reports.bootstrap import (
    get_daily_operational_report,
)


def test_should_build_daily_operational_report():

    assert isinstance(
        get_daily_operational_report,
        GetDailyOperationalReport,
    )
