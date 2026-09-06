from __future__ import annotations

from app.foundation.database import SessionLocal

from app.domains.locations.repositories.sqlite_physical_location_repository import (
    SQLitePhysicalLocationRepository,
)
from app.domains.locations.use_cases.find_all_physical_locations.find_all_physical_locations import (
    FindAllPhysicalLocations,
)
from app.domains.locations.use_cases.find_physical_location_by_code.find_physical_location_by_code import (
    FindPhysicalLocationByCode,
)
from app.domains.locations.use_cases.register_physical_location.register_physical_location import (
    RegisterPhysicalLocation,
)

from .demo_physical_location_seeder import (
    DemoPhysicalLocationSeeder,
)


repository = SQLitePhysicalLocationRepository(
    SessionLocal
)


def load_demo_physical_locations() -> None:
    DemoPhysicalLocationSeeder.load(
        repository=repository,
    )


find_all_physical_locations = (
    FindAllPhysicalLocations(
        repository
    )
)

find_physical_location_by_code = (
    FindPhysicalLocationByCode(
        repository
    )
)

register_physical_location = (
    RegisterPhysicalLocation(
        repository
    )
)
