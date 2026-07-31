from app.domains.assets.value_objects.asset_identity import (
    AssetIdentity,
)


def test_create_asset_identity():

    identity = AssetIdentity(
        code="S2-480-ES09-T269",
        name="TABLERO GENERAL ES09",
        manufacturer="Schneider Electric",
        brand="Square D",
        model="NQOD",
        serial_number="ABC123456",
    )

    assert identity.code == "S2-480-ES09-T269"

    assert identity.name == "TABLERO GENERAL ES09"

    assert identity.manufacturer == "Schneider Electric"

    assert identity.brand == "Square D"

    assert identity.model == "NQOD"

    assert identity.serial_number == "ABC123456"


def test_asset_identity_is_read_only():

    identity = AssetIdentity(
        code="A1",
        name="Motor",
        manufacturer="WEG",
        brand="WEG",
        model="W22",
        serial_number="001",
    )

    assert identity.code == "A1"

    assert identity.name == "Motor"

    def test_asset_identity_equality():

        left = AssetIdentity(
            code="A1",
            name="Motor",
            manufacturer="WEG",
            brand="WEG",
            model="W22",
            serial_number="001",
        )

        right = AssetIdentity(
            code="A1",
            name="Motor",
            manufacturer="WEG",
            brand="WEG",
            model="W22",
            serial_number="001",
        )

        assert left == right

    def test_asset_identity_repr():

        identity = AssetIdentity(
            code="A1",
            name="Motor",
            manufacturer="WEG",
            brand="WEG",
            model="W22",
            serial_number="001",
        )

        assert "AssetIdentity" in repr(identity)

        assert "A1" in repr(identity)
