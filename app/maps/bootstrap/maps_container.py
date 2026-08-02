from __future__ import annotations

from app.maps.repositories.sqlite_map_location_repository import (
    SQLiteMapLocationRepository,
)
from app.maps.use_cases.find_all_map_locations.find_all_map_locations import (
    FindAllMapLocations,
)


map_location_repository = SQLiteMapLocationRepository()

find_all_map_locations = FindAllMapLocations(
    map_location_repository,
)