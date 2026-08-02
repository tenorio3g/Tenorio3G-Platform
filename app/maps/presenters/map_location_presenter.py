from __future__ import annotations

from app.maps.models.map_location import MapLocation


class MapLocationPresenter:
    """
    Convierte ubicaciones persistentes en datos serializables.
    """

    @staticmethod
    def present_many(
        locations: list[MapLocation],
    ) -> list[dict[str, object]]:

        return [
            {
                "asset_code": location.asset_code,
                "name": location.name,
                "category": location.category,
                "x": location.x,
                "y": location.y,
            }
            for location in locations
        ]