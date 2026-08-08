from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
    SparePart,
)

from app.domains.assets.spare_parts.repositories import (
    InMemorySparePartRepository,
)

from app.domains.assets.spare_parts.use_cases.get_spare_parts_by_asset import (
    GetSparePartsByAsset,
    GetSparePartsByAssetQuery,
)


def test_should_get_spare_parts_by_asset() -> None:

    repository = InMemorySparePartRepository()

    bearing = SparePart(
        code="BRG-6206",
        name="Balero 6206",
        manufacturer="SKF",
    )

    belt = SparePart(
        code="BELT-B90",
        name="Banda B-90",
        manufacturer="Gates",
    )

    repository.link_to_asset(
        AssetSparePart(
            asset_code="AHA-24",
            spare_part=bearing,
            quantity=1,
            position="Motor",
        )
    )

    repository.link_to_asset(
        AssetSparePart(
            asset_code="AHA-24",
            spare_part=belt,
            quantity=2,
            position="Transmisión",
        )
    )

    use_case = GetSparePartsByAsset(
        repository
    )

    result = use_case.execute(
        GetSparePartsByAssetQuery(
            asset_code="AHA-24",
        )
    )

    assert result.success is True
    assert len(result.spare_parts) == 2

    codes = {
        relation.spare_part_code
        for relation in result.spare_parts
    }

    assert codes == {
        "BRG-6206",
        "BELT-B90",
    }


def test_should_fail_without_asset_code() -> None:

    repository = InMemorySparePartRepository()

    use_case = GetSparePartsByAsset(
        repository
    )

    result = use_case.execute(
        GetSparePartsByAssetQuery(
            asset_code="",
        )
    )

    assert result.success is False
    assert result.spare_parts == []
    assert result.message == (
        "El código del activo es obligatorio."
    )