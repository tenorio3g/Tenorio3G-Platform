from app.foundation.database import Base, engine

from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
    SparePart,
)

from app.domains.assets.spare_parts.models import (
    AssetSparePartModel,
    SparePartModel,
)

from app.domains.assets.spare_parts.repositories.sqlite_spare_part_repository import (
    SQLiteSparePartRepository,
)


def test_should_save_and_get_spare_part() -> None:

    Base.metadata.create_all(engine)

    repository = SQLiteSparePartRepository()

    repository.save_spare_part(
        SparePart(
            code="TEST-BRG-6206",
            name="Balero 6206",
            manufacturer="SKF",
            part_number="6206-2RS",
            unit="pieza",
            description="Balero de prueba.",
        )
    )

    persisted = repository.get_spare_part_by_code(
        "TEST-BRG-6206",
    )

    assert persisted is not None
    assert persisted.code == "TEST-BRG-6206"
    assert persisted.name == "Balero 6206"
    assert persisted.manufacturer == "SKF"
    assert persisted.part_number == "6206-2RS"


def test_should_link_spare_part_to_asset() -> None:

    Base.metadata.create_all(engine)

    repository = SQLiteSparePartRepository()

    spare_part = SparePart(
        code="TEST-BELT-B90",
        name="Banda B-90",
        manufacturer="Gates",
        part_number="B-90",
    )

    relation = AssetSparePart(
        asset_code="TEST-AHA-24",
        spare_part=spare_part,
        quantity=2,
        position="Transmisión principal",
        observations="Cambiar ambas bandas juntas.",
        is_critical=True,
    )

    repository.link_to_asset(relation)

    relations = repository.get_by_asset_code(
        "TEST-AHA-24",
    )

    matching = [
        relation
        for relation in relations
        if relation.spare_part_code == "TEST-BELT-B90"
    ]

    assert len(matching) == 1

    persisted = matching[0]

    assert persisted.asset_code == "TEST-AHA-24"
    assert persisted.spare_part_code == "TEST-BELT-B90"
    assert persisted.quantity == 2
    assert persisted.position == "Transmisión principal"
    assert persisted.is_critical is True


def test_should_get_assets_by_spare_part_code() -> None:

    Base.metadata.create_all(engine)

    repository = SQLiteSparePartRepository()

    spare_part = SparePart(
        code="TEST-BRG-6308",
        name="Balero 6308",
        manufacturer="SKF",
    )

    repository.link_to_asset(
        AssetSparePart(
            asset_code="TEST-AHA-24",
            spare_part=spare_part,
            quantity=1,
        )
    )

    repository.link_to_asset(
        AssetSparePart(
            asset_code="TEST-AHA-18",
            spare_part=spare_part,
            quantity=1,
        )
    )

    relations = repository.get_assets_by_spare_part_code(
        "TEST-BRG-6308",
    )

    asset_codes = {
        relation.asset_code
        for relation in relations
    }

    assert {
        "TEST-AHA-24",
        "TEST-AHA-18",
    }.issubset(asset_codes)


def test_should_update_existing_asset_relation() -> None:

    Base.metadata.create_all(engine)

    repository = SQLiteSparePartRepository()

    spare_part = SparePart(
        code="TEST-BRG-6206-UPD",
        name="Balero 6206",
    )

    repository.link_to_asset(
        AssetSparePart(
            asset_code="TEST-AHA-24-UPD",
            spare_part=spare_part,
            quantity=1,
            position="Motor",
            is_critical=False,
        )
    )

    repository.link_to_asset(
        AssetSparePart(
            asset_code="TEST-AHA-24-UPD",
            spare_part=spare_part,
            quantity=2,
            position="Motor principal",
            observations="Reemplazar por pares.",
            is_critical=True,
        )
    )

    relations = repository.get_by_asset_code(
        "TEST-AHA-24-UPD",
    )

    matching = [
        relation
        for relation in relations
        if (
            relation.spare_part_code
            == "TEST-BRG-6206-UPD"
        )
    ]

    assert len(matching) == 1

    persisted = matching[0]

    assert persisted.quantity == 2
    assert persisted.position == "Motor principal"
    assert persisted.observations == (
        "Reemplazar por pares."
    )
    assert persisted.is_critical is True