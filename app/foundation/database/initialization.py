from __future__ import annotations

from app.foundation.database.connection import engine
from app.foundation.database.metadata import Base

# Importar este modulo registra todos los modelos ORM
# dentro de Base.metadata.
from app.foundation.database import model_registry  # noqa: F401
from app.foundation.database.migrations.assets_installation_date_nullable import (
    migrate_assets_installation_date_nullable,
)
from app.foundation.database.migrations.map_locations_layer import (
    migrate_map_locations_layer,
)
from app.foundation.database.migrations.map_locations_plan import (
    migrate_map_locations_plan,
)


def initialize_database() -> None:
    """
    Inicializa el esquema persistente de Tenorio3G.

    Crea las tablas registradas en Base.metadata que todavia
    no existen en la base de datos configurada.

    Ejecuta tambien las migraciones incrementales necesarias
    para preservar compatibilidad con bases existentes.

    No elimina tablas ni reemplaza datos existentes.
    """

    Base.metadata.create_all(
        bind=engine
    )

    migrate_assets_installation_date_nullable(
        engine
    )

    migrate_map_locations_layer(
        engine
    )

    migrate_map_locations_plan(
        engine
    )
