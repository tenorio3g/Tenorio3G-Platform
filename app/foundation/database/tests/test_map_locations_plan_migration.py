from __future__ import annotations

from sqlalchemy import create_engine

from app.foundation.database.migrations.map_locations_plan import (
    migrate_map_locations_plan,
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
                layer_code VARCHAR(80)
                    NOT NULL DEFAULT 'electrical',
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
                y,
                layer_code
            )
            VALUES
                (
                    1,
                    'T001',
                    'Tablero T001',
                    'panel',
                    25.5,
                    40.25,
                    'electrical'
                ),
                (
                    2,
                    'CHILLER-01',
                    'Chiller 01',
                    'equipment',
                    72.75,
                    18.5,
                    'hvac'
                )
            """
        )


def test_should_add_plan_code_preserving_existing_locations(
    tmp_path,
) -> None:
    database_path = (
        tmp_path / "legacy_map_locations_plan.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    _create_legacy_map_locations_table(
        engine
    )

    migrate_map_locations_plan(
        engine
    )

    with engine.connect() as connection:
        columns = {
            row[1]: row
            for row in connection.exec_driver_sql(
                "PRAGMA table_info(map_locations)"
            ).fetchall()
        }

        assert "plan_code" in columns
        assert columns["plan_code"][3] == 1

        locations = connection.exec_driver_sql(
            """
            SELECT
                id,
                asset_code,
                name,
                category,
                x,
                y,
                layer_code,
                plan_code
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
                "ground_floor",
            ),
            (
                2,
                "CHILLER-01",
                "Chiller 01",
                "equipment",
                72.75,
                18.5,
                "hvac",
                "ground_floor",
            ),
        ]

    engine.dispose()


def test_should_preserve_asset_code_unique_index(
    tmp_path,
) -> None:
    database_path = (
        tmp_path / "map_locations_plan_index.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    _create_legacy_map_locations_table(
        engine
    )

    migrate_map_locations_plan(
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
        tmp_path / "map_locations_plan_idempotent.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    _create_legacy_map_locations_table(
        engine
    )

    migrate_map_locations_plan(
        engine
    )
    migrate_map_locations_plan(
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
            "plan_code"
        ) == 1

        rows = connection.exec_driver_sql(
            """
            SELECT
                asset_code,
                layer_code,
                plan_code
            FROM map_locations
            ORDER BY id
            """
        ).fetchall()

        assert rows == [
            (
                "T001",
                "electrical",
                "ground_floor",
            ),
            (
                "CHILLER-01",
                "hvac",
                "ground_floor",
            ),
        ]

    engine.dispose()


def test_should_do_nothing_when_table_does_not_exist(
    tmp_path,
) -> None:
    database_path = (
        tmp_path / "without_map_locations_plan.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    migrate_map_locations_plan(
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
