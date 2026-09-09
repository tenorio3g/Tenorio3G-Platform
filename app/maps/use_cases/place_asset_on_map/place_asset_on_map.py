from __future__ import annotations

from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)
from app.maps.models.map_location import (
    MapLocation,
)
from app.maps.repositories.map_layer_repository import (
    MapLayerRepository,
)
from app.maps.repositories.map_location_repository import (
    MapLocationRepository,
)
from app.maps.repositories.map_plan_repository import (
    MapPlanRepository,
)

from .command import PlaceAssetOnMapCommand
from .result import PlaceAssetOnMapResult


class PlaceAssetOnMap:
    def __init__(
        self,
        asset_repository: AssetRepository,
        map_location_repository: MapLocationRepository,
        map_layer_repository: MapLayerRepository,
        map_plan_repository: MapPlanRepository,
    ) -> None:
        self._asset_repository = asset_repository
        self._map_location_repository = (
            map_location_repository
        )
        self._map_layer_repository = (
            map_layer_repository
        )
        self._map_plan_repository = (
            map_plan_repository
        )

    def execute(
        self,
        command: PlaceAssetOnMapCommand,
    ) -> PlaceAssetOnMapResult:
        asset_code = command.asset_code.strip()
        category = command.category.strip()

        asset = self._asset_repository.find_by_code(
            asset_code
        )

        if asset is None:
            return PlaceAssetOnMapResult(
                success=False,
                message=(
                    "No existe el activo indicado."
                ),
            )

        existing_location = (
            self._map_location_repository
            .find_by_asset_code(
                asset_code
            )
        )

        if existing_location is not None:
            return PlaceAssetOnMapResult(
                success=False,
                message=(
                    "El activo ya tiene una "
                    "posicion registrada en el mapa."
                ),
            )

        if not category:
            return PlaceAssetOnMapResult(
                success=False,
                message=(
                    "La categoria del mapa "
                    "es obligatoria."
                ),
            )

        layer = (
            self._map_layer_repository
            .find_by_code(
                command.layer_code
            )
        )

        if layer is None:
            return PlaceAssetOnMapResult(
                success=False,
                message=(
                    "No existe la capa indicada."
                ),
            )

        if not layer.is_active:
            return PlaceAssetOnMapResult(
                success=False,
                message=(
                    "La capa indicada no esta activa."
                ),
            )

        plan = (
            self._map_plan_repository
            .find_by_code(
                command.plan_code
            )
        )

        if plan is None:
            return PlaceAssetOnMapResult(
                success=False,
                message=(
                    "No existe el plano indicado."
                ),
            )

        if not plan.is_active:
            return PlaceAssetOnMapResult(
                success=False,
                message=(
                    "El plano indicado no esta activo."
                ),
            )

        if not self._coordinates_are_valid(
            command.x,
            command.y,
        ):
            return PlaceAssetOnMapResult(
                success=False,
                message=(
                    "Las coordenadas deben estar "
                    "entre 0 y 100."
                ),
            )

        location = MapLocation(
            asset_code=asset.code,
            name=asset.name,
            category=category,
            x=command.x,
            y=command.y,
            layer_code=command.layer_code,
            plan_code=command.plan_code,
        )

        self._map_location_repository.save(
            location
        )

        return PlaceAssetOnMapResult(
            success=True,
            message=(
                "Activo colocado correctamente "
                "en el mapa."
            ),
            location=location,
        )

    @staticmethod
    def _coordinates_are_valid(
        x: float,
        y: float,
    ) -> bool:
        return (
            0.0 <= x <= 100.0
            and
            0.0 <= y <= 100.0
        )
