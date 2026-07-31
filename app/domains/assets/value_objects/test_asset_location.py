from app.domains.assets.value_objects.asset_location import (
    AssetLocation,
)

import pytest


def test_create_asset_location():

    location = AssetLocation(
        code="MD2-PA-SMT-001",
    )

    assert location.code == "MD2-PA-SMT-001"


def test_location_code_is_trimmed():

    location = AssetLocation(
        code="   MD2-01   ",
    )

    assert location.code == "MD2-01"


def test_location_code_is_required():

    with pytest.raises(ValueError):

        AssetLocation(
            code="   ",
        )