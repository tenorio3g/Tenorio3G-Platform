from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
    SparePart,
)
from app.domains.assets.spare_parts.repositories import (
    InMemorySparePartRepository,
)


def test_should_save_and_get_spare_part() -> None:
    repository = InMemorySparePartRepository()

    spare_part = SparePart(
        code="BRG-6206",
        name="Balero 6206",
        manufacturer="SKF",
        part_number="6206-2RS",
    )

    repository.save_spare_part(spare_part)

    persisted = repository.get_spare_part_by_code(
        "BRG-6206",
    )

    assert persisted is not None
    assert persisted.code == "BRG-6206"
    assert persisted.name == "Balero 6206"
    assert persisted.manufacturer == "SKF"


def test_should_link_spare_part_to_asset() -> None:
    repository = InMemorySparePartRepository()

    spare_part = SparePart(
        code="BELT-B90",
        name="Banda B-90",
    )

    repository.save_spare_part(spare_part)

    relation = AssetSparePart(
        asset_code="AHA-24",
        spare_part=spare_part,
        quantity=2,
        position="Transmisión principal",
        observations="Cambiar ambas bandas juntas.",
        is_critical=True,
    )

    repository.link_to_asset(relation)

    relations = repository.get_by_asset_code(
        "AHA-24",
    )

    assert len(relations) == 1
    assert relations[0].spare_part_code == "BELT-B90"
    assert relations[0].quantity == 2
    assert relations[0].is_critical is True


def test_should_get_assets_by_spare_part_code() -> None:
    repository = InMemorySparePartRepository()

    spare_part = SparePart(
        code="BRG-6308",
        name="Balero 6308",
    )

    repository.save_spare_part(spare_part)

    repository.link_to_asset(
        AssetSparePart(
            asset_code="AHA-24",
            spare_part=spare_part,
            quantity=1,
        )
    )

    repository.link_to_asset(
        AssetSparePart(
            asset_code="AHA-18",
            spare_part=spare_part,
            quantity=1,
        )
    )

    relations = repository.get_assets_by_spare_part_code(
        "BRG-6308",
    )

    asset_codes = {
        relation.asset_code
        for relation in relations
    }

    assert len(relations) == 2
    assert asset_codes == {
        "AHA-24",
        "AHA-18",
    }


def test_should_update_existing_asset_relation() -> None:
    repository = InMemorySparePartRepository()

    spare_part = SparePart(
        code="BELT-B90",
        name="Banda B-90",
    )

    repository.save_spare_part(spare_part)

    repository.link_to_asset(
        AssetSparePart(
            asset_code="AHA-24",
            spare_part=spare_part,
            quantity=1,
            position="Transmisión",
            is_critical=False,
        )
    )

    repository.link_to_asset(
        AssetSparePart(
            asset_code="AHA-24",
            spare_part=spare_part,
            quantity=2,
            position="Transmisión principal",
            observations="Reemplazar por pares.",
            is_critical=True,
        )
    )

    relations = repository.get_by_asset_code(
        "AHA-24",
    )

    assert len(relations) == 1
    assert relations[0].quantity == 2
    assert relations[0].position == (
        "Transmisión principal"
    )
    assert relations[0].observations == (
        "Reemplazar por pares."
    )
    assert relations[0].is_critical is True