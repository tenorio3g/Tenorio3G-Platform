from __future__ import annotations

from sqlalchemy.engine import Engine


DEFAULT_MAP_LAYER_CODE = "electrical"


def migrate_map_locations_layer(
    engine: Engine,
) -> None:
    """
    Agrega layer_code a map_locations existentes.

    Las ubicaciones heredadas se asignan a la capa
    electrical sin modificar sus demas datos.

    La migracion es idempotente.
    """

    with engine.begin() as connection:
        table_exists = connection.exec_driver_sql(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'map_locations'
            """
        ).fetchone()

        if table_exists is None:
            return

        columns = {
            row[1]
            for row in connection.exec_driver_sql(
                "PRAGMA table_info(map_locations)"
            ).fetchall()
        }

        if "layer_code" in columns:
            return

        connection.exec_driver_sql(
            """
            ALTER TABLE map_locations
            ADD COLUMN layer_code VARCHAR(80)
            NOT NULL DEFAULT 'electrical'
            """
        )
