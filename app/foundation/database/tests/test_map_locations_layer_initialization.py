from __future__ import annotations

from importlib import import_module

from sqlalchemy import create_engine


initialization = import_module(
    "app.foundation.database.initialization"
)


def test_initialize_database_should_migrate_map_locations(
    tmp_path,
    monkeypatch,
) -> None:
    database_path = (
        tmp_path / "legacy_maps_initialization.db"
    )

    test_engine = create_engine(
        f"sqlite:///{database_path}",
        future=True,
    )

    with test_engine.begin() as connection:
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
            INSERT INTO map_locations (
                id,
                asset_code,
                name,
                category,
                x,
                y
            )
            VALUES (
                1,
                'T269',
                'Tablero General ES09',
                'panel',
                72.75,
                18.5
            )
            """
        )

    monkeypatch.setattr(
        initialization,
        "engine",
        test_engine,
    )

    initialization.initialize_database()

    with test_engine.connect() as connection:
        row = connection.exec_driver_sql(
            """
            SELECT
                asset_code,
                x,
                y,
                layer_code,
                plan_code
            FROM map_locations
            WHERE asset_code = 'T269'
            """
        ).fetchone()

        assert row == (
            "T269",
            72.75,
            18.5,
            "electrical",
            "ground_floor",
        )

    test_engine.dispose()
