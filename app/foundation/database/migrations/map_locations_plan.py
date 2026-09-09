from __future__ import annotations

from sqlalchemy.engine import Engine


DEFAULT_MAP_PLAN_CODE = "ground_floor"


def migrate_map_locations_plan(
    engine: Engine,
) -> None:
    """
    Agrega plan_code a map_locations existentes.

    Las ubicaciones heredadas se asignan al plano
    ground_floor sin modificar sus demas datos.

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

        if "plan_code" in columns:
            return

        connection.exec_driver_sql(
            """
            ALTER TABLE map_locations
            ADD COLUMN plan_code VARCHAR(80)
            NOT NULL DEFAULT 'ground_floor'
            """
        )
