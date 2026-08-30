from datetime import datetime, timedelta

from app.domains.operational_intelligence.queries import (
    ApprovalLeadTimeItem,
    GetApprovalLeadTimeSummary,
)


def create_item(
    work_order_code: str,
    lead_time: timedelta,
) -> ApprovalLeadTimeItem:

    created_at = datetime(
        2026,
        8,
        20,
        8,
        0,
    )

    return ApprovalLeadTimeItem(
        work_order_code=work_order_code,
        created_at=created_at,
        approved_at=(
            created_at + lead_time
        ),
        lead_time=lead_time,
    )


def test_should_return_empty_summary():

    use_case = GetApprovalLeadTimeSummary()

    result = use_case.execute([])

    assert result.total_approved == 0
    assert result.average_lead_time is None
    assert result.minimum_lead_time is None
    assert result.maximum_lead_time is None


def test_should_count_approved_work_orders():

    use_case = GetApprovalLeadTimeSummary()

    items = [
        create_item(
            "WO-001",
            timedelta(hours=2),
        ),
        create_item(
            "WO-002",
            timedelta(hours=4),
        ),
        create_item(
            "WO-003",
            timedelta(hours=6),
        ),
    ]

    result = use_case.execute(items)

    assert result.total_approved == 3


def test_should_calculate_average_lead_time():

    use_case = GetApprovalLeadTimeSummary()

    items = [
        create_item(
            "WO-001",
            timedelta(hours=2),
        ),
        create_item(
            "WO-002",
            timedelta(hours=4),
        ),
        create_item(
            "WO-003",
            timedelta(hours=6),
        ),
    ]

    result = use_case.execute(items)

    assert (
        result.average_lead_time
        == timedelta(hours=4)
    )


def test_should_calculate_minimum_and_maximum_lead_time():

    use_case = GetApprovalLeadTimeSummary()

    items = [
        create_item(
            "WO-001",
            timedelta(hours=8),
        ),
        create_item(
            "WO-002",
            timedelta(hours=2),
        ),
        create_item(
            "WO-003",
            timedelta(hours=12),
        ),
        create_item(
            "WO-004",
            timedelta(hours=5),
        ),
    ]

    result = use_case.execute(items)

    assert (
        result.minimum_lead_time
        == timedelta(hours=2)
    )

    assert (
        result.maximum_lead_time
        == timedelta(hours=12)
    )
