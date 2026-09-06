from __future__ import annotations

from app.foundation.database.connection import engine
from app.foundation.database.metadata import Base

# Importar este m?dulo registra todos los modelos ORM
# dentro de Base.metadata.
from app.foundation.database import model_registry  # noqa: F401
from app.foundation.database.migrations.assets_installation_date_nullable import (
    migrate_assets_installation_date_nullable,
)

from app.foundation.database import model_registry  # noqa: F401

def initialize_database() -> None:
    """
    Inicializa el esquema persistente de Tenorio3G.

    Crea las tablas registradas en Base.metadata que todav?a
    no existen en la base de datos configurada.

    No elimina tablas ni reemplaza datos existentes.
    """
    Base.metadata.create_all(
        bind=engine
    )
    migrate_assets_installation_date_nullable(
        engine
    )
