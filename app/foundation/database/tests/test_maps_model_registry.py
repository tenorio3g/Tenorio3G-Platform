from __future__ import annotations

from importlib import import_module

from app.foundation.database.metadata import Base


def test_should_register_maps_models_in_metadata() -> None:
    import_module(
        "app.foundation.database.model_registry"
    )

    assert "map_locations" in Base.metadata.tables
    assert "map_layers" in Base.metadata.tables
    assert "map_plans" in Base.metadata.tables
