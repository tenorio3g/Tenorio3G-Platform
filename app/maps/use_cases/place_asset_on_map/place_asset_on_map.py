from __future__ import annotations

from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)
from app.maps.models.map_location import (
    MapLocation,
)
from app.maps.repositories.map_location_repository import (
    MapLocationRepository,
)

from .command import PlaceAssetOnMapCommand
from .result import PlaceAssetOnMapResult


class PlaceAssetOnMap:
    def __init__(
        self,
        asset_repository: AssetRepository,
        map_location_repository: MapLocationRepository,
    ) -> None:
        self._asset_repository = asset_repository
        self._map_location_repository = (
            map_location_repository
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
