from __future__ import annotations

from sqlalchemy import create_engine

from app.foundation.database.migrations.map_locations_layer import (
    migrate_map_locations_layer,
)


def _create_legacy_map_locations_table(engine) -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql(
            """
            CREATE TABLE map_locations (
                id INTEGER NOT NULL,
                asset_code VARCHAR(80) NOT NULL,
                name VARCHAR(160) NOT NULL,
                category VARCHAR(50) NOT NULL,
                x FLOAT NOT NULL,
                y FLOAT NOT NULL,
                PRIMARY KEY (id)
            )
            """
        )

        connection.exec_driver_sql(
            """
            CREATE UNIQUE INDEX ix_map_locations_asset_code
            ON map_locations (asset_code)
            """
        )

        connection.exec_driver_sql(
            """
            INSERT INTO map_locations (
                id,
                asset_code,
                name,
                category,
                x,
                y
            )
            VALUES
                (
                    1,
                    'T001',
                    'Tablero T001',
                    'panel',
                    25.5,
                    40.25
                ),
                (
                    2,
                    'T269',
                    'Tablero General ES09',
                    'panel',
                    72.75,
                    18.5
                )
            """
        )


def test_should_add_layer_code_preserving_existing_locations(
    tmp_path,
) -> None:
    database_path = (
        tmp_path / "legacy_map_locations.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    _create_legacy_map_locations_table(
        engine
    )

    migrate_map_locations_layer(
        engine
    )

    with engine.connect() as connection:
        columns = {
            row[1]: row
            for row in connection.exec_driver_sql(
                "PRAGMA table_info(map_locations)"
            ).fetchall()
        }

        assert "layer_code" in columns
        assert columns["layer_code"][3] == 1

        locations = connection.exec_driver_sql(
            """
            SELECT
                id,
                asset_code,
                name,
                category,
                x,
                y,
                layer_code
            FROM map_locations
            ORDER BY id
            """
        ).fetchall()

        assert locations == [
            (
                1,
                "T001",
                "Tablero T001",
                "panel",
                25.5,
                40.25,
                "electrical",
            ),
            (
                2,
                "T269",
                "Tablero General ES09",
                "panel",
                72.75,
                18.5,
                "electrical",
            ),
        ]

    engine.dispose()


def test_should_preserve_asset_code_unique_index(
    tmp_path,
) -> None:
    database_path = (
        tmp_path / "map_locations_index.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    _create_legacy_map_locations_table(
        engine
    )

    migrate_map_locations_layer(
        engine
    )

    with engine.connect() as connection:
        indexes = {
            row[1]
            for row in connection.exec_driver_sql(
                "PRAGMA index_list(map_locations)"
            ).fetchall()
        }

        assert (
            "ix_map_locations_asset_code"
            in indexes
        )

    engine.dispose()


def test_should_be_idempotent(
    tmp_path,
) -> None:
    database_path = (
        tmp_path / "map_locations_idempotent.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    _create_legacy_map_locations_table(
        engine
    )

    migrate_map_locations_layer(
        engine
    )
    migrate_map_locations_layer(
        engine
    )

    with engine.connect() as connection:
        columns = [
            row[1]
            for row in connection.exec_driver_sql(
                "PRAGMA table_info(map_locations)"
            ).fetchall()
        ]

        assert columns.count(
            "layer_code"
        ) == 1

        layer_codes = connection.exec_driver_sql(
            """
            SELECT layer_code
            FROM map_locations
            ORDER BY id
            """
        ).fetchall()

        assert layer_codes == [
            ("electrical",),
            ("electrical",),
        ]

    engine.dispose()


def test_should_do_nothing_when_table_does_not_exist(
    tmp_path,
) -> None:
    database_path = (
        tmp_path / "without_map_locations.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    migrate_map_locations_layer(
        engine
    )

    with engine.connect() as connection:
        table = connection.exec_driver_sql(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'map_locations'
            """
        ).fetchone()

        assert table is None

    engine.dispose()
