from __future__ import annotations

from app.foundation.database import SessionLocal

from app.domains.assets.bootstrap import (
    repository as asset_repository,
)

from app.maps.repositories.sqlite_map_location_repository import (
    SQLiteMapLocationRepository,
)

from app.maps.use_cases.find_all_map_locations.find_all_map_locations import (
    FindAllMapLocations,
)

from app.maps.use_cases.place_asset_on_map.place_asset_on_map import (
    PlaceAssetOnMap,
)

from app.maps.use_cases.move_asset_on_map.move_asset_on_map import (
    MoveAssetOnMap,
)


map_location_repository = (
    SQLiteMapLocationRepository(
        SessionLocal
    )
)

find_all_map_locations = (
    FindAllMapLocations(
        map_location_repository
    )
)

place_asset_on_map = (
    PlaceAssetOnMap(
        asset_repository,
        map_location_repository,
    )
)

move_asset_on_map = (
    MoveAssetOnMap(
        map_location_repository
    )
)
