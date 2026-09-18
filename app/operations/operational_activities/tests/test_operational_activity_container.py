from app.operations.operational_activities.bootstrap import (
    complete_operational_activity,
    create_operational_activity,
    operational_activity_repository,
)

from app.operations.operational_activities.repositories import (
    SQLiteOperationalActivityRepository,
)

from app.operations.operational_activities.use_cases import (
    CompleteOperationalActivity,
    CreateOperationalActivity,
)


def test_should_build_operational_activity_repository():

    assert isinstance(
        operational_activity_repository,
        SQLiteOperationalActivityRepository,
    )


def test_should_build_operational_activity_use_cases():

    assert isinstance(
        create_operational_activity,
        CreateOperationalActivity,
    )

    assert isinstance(
        complete_operational_activity,
        CompleteOperationalActivity,
    )
