from __future__ import annotations

from app.maps.models.map_location import (
    MapLocation,
)
from app.maps.presenters.map_location_presenter import (
    MapLocationPresenter,
)


def test_should_present_layer_code() -> None:
    location = MapLocation(
        asset_code="CH-001",
        name="Chiller 1",
        category="chiller",
        x=25.0,
        y=30.0,
        layer_code="hvac",
        plan_code="roof",
    )

    payload = MapLocationPresenter.present_many(
        [location]
    )

    assert payload == [
        {
            "asset_code": "CH-001",
            "layer_code": "hvac",
            "plan_code": "roof",
            "name": "Chiller 1",
            "category": "chiller",
            "x": 25.0,
            "y": 30.0,
        }
    ]
