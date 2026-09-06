from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database.metadata import Base
from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)
from app.domains.locations.models.physical_location_model import (
    PhysicalLocationModel,
)
from app.domains.locations.repositories.sqlite_physical_location_repository import (
    SQLitePhysicalLocationRepository,
)


def create_repository():

    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(
        bind=engine,
    )

    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    repository = SQLitePhysicalLocationRepository(
        session_factory=session_factory,
    )

    return repository, session_factory


def test_save_and_find_physical_location() -> None:

    repository, _ = create_repository()

    repository.save(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura MD1",
            area="MD1",
        )
    )

    location = repository.find_by_code(
        "MD1-PINTURA"
    )

    assert location is not None
    assert location.code == "MD1-PINTURA"
    assert location.name == "Pintura MD1"
    assert location.area == "MD1"
    assert location.is_active is True


def test_find_by_code_returns_none_when_missing() -> None:

    repository, _ = create_repository()

    location = repository.find_by_code(
        "UNKNOWN"
    )

    assert location is None


def test_find_all_orders_locations_by_code() -> None:

    repository, _ = create_repository()

    repository.save(
        PhysicalLocation(
            code="SUBESTACION-NORTE",
            name="Subestacion Norte",
            area="SERVICIOS",
        )
    )

    repository.save(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura MD1",
            area="MD1",
        )
    )

    locations = repository.find_all()

    assert [
        location.code
        for location in locations
    ] == [
        "MD1-PINTURA",
        "SUBESTACION-NORTE",
    ]


def test_save_updates_existing_location() -> None:

    repository, _ = create_repository()

    repository.save(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura MD1",
            area="MD1",
        )
    )

    repository.save(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura Principal",
            area="MD1",
            is_active=False,
        )
    )

    location = repository.find_by_code(
        "MD1-PINTURA"
    )

    assert location is not None
    assert location.name == "Pintura Principal"
    assert location.is_active is False


def test_update_existing_location() -> None:

    repository, _ = create_repository()

    repository.save(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura MD1",
            area="MD1",
        )
    )

    repository.update(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura Actualizada",
            area="MD1",
            is_active=False,
        )
    )

    location = repository.find_by_code(
        "MD1-PINTURA"
    )

    assert location is not None
    assert location.name == "Pintura Actualizada"
    assert location.is_active is False


def test_update_requires_existing_location() -> None:

    repository, _ = create_repository()

    try:
        repository.update(
            PhysicalLocation(
                code="UNKNOWN",
                name="Ubicacion inexistente",
                area="TEST",
            )
        )
    except KeyError as error:
        assert error.args[0] == "UNKNOWN"
    else:
        raise AssertionError(
            "Expected KeyError"
        )


def test_persists_physical_location_model() -> None:

    repository, session_factory = (
        create_repository()
    )

    repository.save(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura MD1",
            area="MD1",
        )
    )

    with session_factory() as session:

        model = session.get(
            PhysicalLocationModel,
            "MD1-PINTURA",
        )

        assert model is not None
        assert model.name == "Pintura MD1"
        assert model.area == "MD1"
        assert model.is_active is True
