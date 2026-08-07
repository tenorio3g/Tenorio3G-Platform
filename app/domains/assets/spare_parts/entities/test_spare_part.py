import pytest

from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
    SparePart,
)


def test_should_create_spare_part() -> None:
    spare_part = SparePart(
        code="BRG-6206",
        name="Balero 6206",
        manufacturer="SKF",
        part_number="6206-2RS",
    )

    assert spare_part.code == "BRG-6206"
    assert spare_part.name == "Balero 6206"
    assert spare_part.manufacturer == "SKF"
    assert spare_part.part_number == "6206-2RS"


def test_should_link_spare_part_to_asset() -> None:
    spare_part = SparePart(
        code="BELT-B90",
        name="Banda B-90",
    )

    relation = AssetSparePart(
        asset_code="AHA-24",
        spare_part=spare_part,
        quantity=2,
        position="Transmisión principal",
        is_critical=True,
    )

    assert relation.asset_code == "AHA-24"
    assert relation.spare_part_code == "BELT-B90"
    assert relation.quantity == 2
    assert relation.is_critical is True


def test_should_reject_invalid_quantity() -> None:
    spare_part = SparePart(
        code="BRG-6308",
        name="Balero 6308",
    )

    with pytest.raises(
        ValueError,
        match="La cantidad debe ser mayor que cero.",
    ):
        AssetSparePart(
            asset_code="AHA-24",
            spare_part=spare_part,
            quantity=0,
        )