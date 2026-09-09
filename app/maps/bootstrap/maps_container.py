from __future__ import annotations

from app.foundation.database import SessionLocal

from app.domains.assets.bootstrap import (
    repository as asset_repository,
)

from app.maps.repositories.sqlite_map_layer_repository import (
    SQLiteMapLayerRepository,
)

from app.maps.repositories.sqlite_map_location_repository import (
    SQLiteMapLocationRepository,
)

from app.maps.repositories.sqlite_map_plan_repository import (
    SQLiteMapPlanRepository,
)

from app.maps.use_cases.ensure_default_map_layers.ensure_default_map_layers import (
    EnsureDefaultMapLayers,
)

from app.maps.use_cases.ensure_default_map_plans.ensure_default_map_plans import (
    EnsureDefaultMapPlans,
)

from app.maps.use_cases.find_all_map_locations.find_all_map_locations import (
    FindAllMapLocations,
)

from app.maps.use_cases.list_active_map_layers.list_active_map_layers import (
    ListActiveMapLayers,
)

from app.maps.use_cases.list_active_map_plans.list_active_map_plans import (
    ListActiveMapPlans,
)

from app.maps.use_cases.place_asset_on_map.place_asset_on_map import (
    PlaceAssetOnMap,
)

from app.maps.use_cases.move_asset_on_map.move_asset_on_map import (
    MoveAssetOnMap,
)


map_layer_repository = (
    SQLiteMapLayerRepository(
        SessionLocal
    )
)

map_location_repository = (
    SQLiteMapLocationRepository(
        SessionLocal
    )
)

map_plan_repository = (
    SQLiteMapPlanRepository(
        SessionLocal
    )
)

ensure_default_map_layers = (
    EnsureDefaultMapLayers(
        map_layer_repository
    )
)

ensure_default_map_plans = (
    EnsureDefaultMapPlans(
        map_plan_repository
    )
)

find_all_map_locations = (
    FindAllMapLocations(
        map_location_repository
    )
)

list_active_map_layers = (
    ListActiveMapLayers(
        map_layer_repository
    )
)

list_active_map_plans = (
    ListActiveMapPlans(
        map_plan_repository
    )
)

place_asset_on_map = (
    PlaceAssetOnMap(
        asset_repository,
        map_location_repository,
        map_layer_repository,
        map_plan_repository,
    )
)

move_asset_on_map = (
    MoveAssetOnMap(
        map_location_repository
    )
)
