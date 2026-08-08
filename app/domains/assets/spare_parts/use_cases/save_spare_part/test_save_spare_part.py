from app.domains.assets.spare_parts.repositories import (
    InMemorySparePartRepository,
)

from app.domains.assets.spare_parts.use_cases.save_spare_part import (
    SaveSparePart,
    SaveSparePartCommand,
)


def test_should_save_spare_part_and_link_to_asset() -> None:

    repository = InMemorySparePartRepository()

    use_case = SaveSparePart(
        repository
    )

    result = use_case.execute(
        SaveSparePartCommand(
            asset_code="AHA-24",
            code="BELT-B90",
            name="Banda B-90",
            manufacturer="Gates",
            part_number="B-90",
            unit="pieza",
            quantity=2,
            position="Transmisión principal",
            observations="Cambiar ambas bandas juntas.",
            is_critical=True,
        )
    )

    relations = repository.get_by_asset_code(
        "AHA-24"
    )

    assert result.success is True
    assert len(relations) == 1
    assert relations[0].spare_part_code == "BELT-B90"
    assert relations[0].quantity == 2
    assert relations[0].is_critical is True


def test_should_fail_with_invalid_quantity() -> None:

    repository = InMemorySparePartRepository()

    use_case = SaveSparePart(
        repository
    )

    result = use_case.execute(
        SaveSparePartCommand(
            asset_code="AHA-24",
            code="BRG-6206",
            name="Balero 6206",
            manufacturer="SKF",
            part_number="6206-2RS",
            unit="pieza",
            quantity=0,
            position="Motor",
            observations="",
            is_critical=True,
        )
    )

    assert result.success is False
    assert result.message == (
        "La cantidad debe ser mayor que cero."
    )