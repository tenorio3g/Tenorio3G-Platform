from __future__ import annotations

from sqlalchemy.engine import Engine


def migrate_assets_installation_date_nullable(
    engine: Engine,
) -> None:
    """
    Migra assets.installation_date de NOT NULL a nullable.

    La migracion es idempotente:
    si la tabla no existe o la columna ya permite NULL,
    no realiza cambios.
    """

    with engine.begin() as connection:
        table_exists = connection.exec_driver_sql(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'assets'
            """
        ).fetchone()

        if table_exists is None:
            return

        columns = connection.exec_driver_sql(
            "PRAGMA table_info(assets)"
        ).fetchall()

        installation_date_column = next(
            (
                column
                for column in columns
                if column[1] == "installation_date"
            ),
            None,
        )

        if installation_date_column is None:
            return

        is_not_null = (
            installation_date_column[3] == 1
        )

        if not is_not_null:
            return

        connection.exec_driver_sql(
            """
            ALTER TABLE assets
            RENAME TO assets_legacy_installation_date
            """
        )

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
            SELECT
                code,
                name,
                asset_model_code,
                serial_number,
                location_code,
                status,
                installation_date,
                deactivation_reason
            FROM assets_legacy_installation_date
            """
        )

        connection.exec_driver_sql(
            """
            DROP TABLE assets_legacy_installation_date
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
