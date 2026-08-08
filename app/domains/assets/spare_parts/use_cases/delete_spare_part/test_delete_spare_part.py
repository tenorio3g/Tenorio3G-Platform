from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
    SparePart,
)

from app.domains.assets.spare_parts.repositories import (
    InMemorySparePartRepository,
)

from app.domains.assets.spare_parts.use_cases.delete_spare_part import (
    DeleteSparePart,
    DeleteSparePartCommand,
)


def test_should_delete_spare_part_from_asset():

    repository = InMemorySparePartRepository()

    spare_part = SparePart(
        code="6206",
        name="Balero",
        manufacturer="SKF",
        part_number="6206-2RS",
        unit="pieza",
    )

    repository.save_spare_part(
        spare_part
    )

    repository.link_to_asset(
        AssetSparePart(
            asset_code="ES09",
            spare_part=spare_part,
            quantity=2,
            position="Motor",
            observations="",
            is_critical=True,
        )
    )

    use_case = DeleteSparePart(
        repository
    )

    result = use_case.execute(
        DeleteSparePartCommand(
            asset_code="ES09",
            spare_part_code="6206",
        )
    )

    relations = repository.get_by_asset_code(
        "ES09"
    )

    assert result.success is True
    assert len(relations) == 0