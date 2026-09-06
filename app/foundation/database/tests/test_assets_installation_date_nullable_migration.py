from __future__ import annotations

from sqlalchemy import (
    create_engine,
)

from app.foundation.database.migrations.assets_installation_date_nullable import (
    migrate_assets_installation_date_nullable,
)


def test_should_make_asset_installation_date_nullable_preserving_data_and_indexes(
    tmp_path,
) -> None:
    database_path = (
        tmp_path / "legacy_assets.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    with engine.begin() as connection:
        connection.exec_driver_sql(
            """
            CREATE TABLE assets (
                code VARCHAR(100) NOT NULL,
                name VARCHAR(255) NOT NULL,
                asset_model_code VARCHAR(100) NOT NULL,
                serial_number VARCHAR(255) NOT NULL,
                location_code VARCHAR(100) NOT NULL,
                status VARCHAR(100) NOT NULL,
                installation_date DATE NOT NULL,
                deactivation_reason VARCHAR(1000),
                PRIMARY KEY (code)
            )
            """
        )

        connection.exec_driver_sql(
            """
            CREATE INDEX ix_assets_asset_model_code
            ON assets (asset_model_code)
            """
        )

        connection.exec_driver_sql(
            """
            CREATE INDEX ix_assets_location_code
            ON assets (location_code)
            """
        )

        connection.exec_driver_sql(
            """
            CREATE INDEX ix_assets_status
            ON assets (status)
            """
        )

        connection.exec_driver_sql(
            """
            INSERT INTO assets (
                code,
                name,
                asset_model_code,
                serial_number,
                location_code,
                status,
                installation_date,
                deactivation_reason
            )
            VALUES (
                'ASSET-001',
                'Existing Asset',
                'MODEL-001',
                '',
                'LOC-001',
                'OPERATING',
                '2026-01-15',
                NULL
            )
            """
        )

    migrate_assets_installation_date_nullable(
        engine
    )

    with engine.connect() as connection:
        columns = {
            row[1]: row
            for row in connection.exec_driver_sql(
                "PRAGMA table_info(assets)"
            ).fetchall()
        }

        assert (
            columns["installation_date"][3]
            == 0
        )

        asset = connection.exec_driver_sql(
            """
            SELECT
                code,
                name,
                asset_model_code,
                serial_number,
                location_code,
                status,
                installation_date,
                deactivation_reason
            FROM assets
            WHERE code = 'ASSET-001'
            """
        ).fetchone()

        assert asset is not None
        assert asset[0] == "ASSET-001"
        assert asset[1] == "Existing Asset"
        assert asset[2] == "MODEL-001"
        assert asset[3] == ""
        assert asset[4] == "LOC-001"
        assert asset[5] == "OPERATING"
        assert asset[6] == "2026-01-15"
        assert asset[7] is None

        indexes = {
            row[0]
            for row in connection.exec_driver_sql(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'index'
                  AND tbl_name = 'assets'
                """
            ).fetchall()
        }

        assert (
            "ix_assets_asset_model_code"
            in indexes
        )
        assert (
            "ix_assets_location_code"
            in indexes
        )
        assert (
            "ix_assets_status"
            in indexes
        )

    engine.dispose()
def test_should_be_idempotent_when_installation_date_is_already_nullable(
    tmp_path,
) -> None:
    database_path = (
        tmp_path / "nullable_assets.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    with engine.begin() as connection:
        connection.exec_driver_sql(
            """
            CREATE TABLE assets (
                code VARCHAR(100) NOT NULL,
                name VARCHAR(255) NOT NULL,
                asset_model_code VARCHAR(100) NOT NULL,
                serial_number VARCHAR(255) NOT NULL,
                location_code VARCHAR(100) NOT NULL,
                status VARCHAR(100) NOT NULL,
                installation_date DATE,
                deactivation_reason VARCHAR(1000),
                PRIMARY KEY (code)
            )
            """
        )

        connection.exec_driver_sql(
            """
            CREATE INDEX ix_assets_asset_model_code
            ON assets (asset_model_code)
            """
        )

        connection.exec_driver_sql(
            """
            CREATE INDEX ix_assets_location_code
            ON assets (location_code)
            """
        )

        connection.exec_driver_sql(
            """
            CREATE INDEX ix_assets_status
            ON assets (status)
            """
        )

        connection.exec_driver_sql(
            """
            INSERT INTO assets (
                code,
                name,
                asset_model_code,
                serial_number,
                location_code,
                status,
                installation_date,
                deactivation_reason
            )
            VALUES (
                'ASSET-002',
                'Asset Without Date',
                'MODEL-002',
                '',
                'LOC-002',
                'OPERATING',
                NULL,
                NULL
            )
            """
        )

    migrate_assets_installation_date_nullable(
        engine
    )

    migrate_assets_installation_date_nullable(
        engine
    )

    with engine.connect() as connection:
        columns = {
            row[1]: row
            for row in connection.exec_driver_sql(
                "PRAGMA table_info(assets)"
            ).fetchall()
        }

        assert (
            columns["installation_date"][3]
            == 0
        )

        asset = connection.exec_driver_sql(
            """
            SELECT
                code,
                installation_date
            FROM assets
            WHERE code = 'ASSET-002'
            """
        ).fetchone()

        assert asset is not None
        assert asset[0] == "ASSET-002"
        assert asset[1] is None

    engine.dispose()
