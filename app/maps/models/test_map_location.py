from sqlalchemy import select

from app.foundation.database import (
    Base,
    SessionLocal,
    engine,
)
from app.maps.models.map_location import MapLocation


def test_should_persist_map_location() -> None:

    Base.metadata.create_all(engine)

    location = MapLocation(
        asset_code="S2-480-ES09-T269",
        name="TABLERO GENERAL ES09",
        category="tableros",
        x=52.4,
        y=38.7,
    )

    with SessionLocal() as session:

        existing = session.scalar(
            select(MapLocation).where(
                MapLocation.asset_code
                == "S2-480-ES09-T269"
            )
        )

        if existing is not None:
            session.delete(existing)
            session.commit()

        session.add(location)
        session.commit()

        persisted = session.scalar(
            select(MapLocation).where(
                MapLocation.asset_code
                == "S2-480-ES09-T269"
            )
        )

        assert persisted is not None
        assert persisted.asset_code == "S2-480-ES09-T269"
        assert persisted.name == "TABLERO GENERAL ES09"
        assert persisted.category == "tableros"
        assert persisted.x == 52.4
        assert persisted.y == 38.7