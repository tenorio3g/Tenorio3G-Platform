from __future__ import annotations

from app.maps.repositories.map_location_repository import (
    MapLocationRepository,
)

from .command import MoveAssetOnMapCommand
from .result import MoveAssetOnMapResult


class MoveAssetOnMap:
    def __init__(
        self,
        repository: MapLocationRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: MoveAssetOnMapCommand,
    ) -> MoveAssetOnMapResult:
        asset_code = command.asset_code.strip()

        location = (
            self._repository.find_by_asset_code(
                asset_code
            )
        )

        if location is None:
            return MoveAssetOnMapResult(
                success=False,
                message=(
                    "El activo no tiene una "
                    "posicion registrada en el mapa."
                ),
            )

        try:
            location.move_to(
                x=command.x,
                y=command.y,
            )
        except ValueError as exc:
            return MoveAssetOnMapResult(
                success=False,
                message=str(exc),
            )

        self._repository.save(
            location
        )

        return MoveAssetOnMapResult(
            success=True,
            message=(
                "Activo reubicado correctamente "
                "en el mapa."
            ),
            location=location,
        )
