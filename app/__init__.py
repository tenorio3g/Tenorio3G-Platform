from flask import Flask

from config.config import Config

from app.identity import identity
from app.assets import assets
from app.core.routes import core
from app.foundation import foundation
from app.foundation.registry import RegistryValidator
from app.operations import operations
from app.work_orders import work_orders
from app.maps import maps

from app.domains.identity.authentication import (
    can,
)

from app.foundation.database.initialization import (
    initialize_database,
)

from app.domains.locations.bootstrap.locations_container import (
    load_demo_physical_locations,
)

from app.domains.assets.bootstrap.assets_container import (
    load_demo_assets,
)

from app.maps.bootstrap import (
    ensure_default_map_layers,
    ensure_default_map_plans,
)


def create_app(config_class=Config) -> Flask:
    """
    Crea y configura la aplicaci?n Flask de Tenorio3G.

    Args:
        config_class:
            Clase de configuraci?n que ser? cargada por Flask.
            Permite utilizar configuraciones diferentes para
            desarrollo, pruebas y producci?n.

    Returns:
        Aplicaci?n Flask completamente configurada.
    """

    app = Flask(__name__)

    app.config.from_object(config_class)
    app.jinja_env.globals["can"] = can

    _initialize_persistence()
    _validate_foundation_registry()
    _register_blueprints(app)

    return app


def _initialize_persistence() -> None:
    """
    Inicializa la persistencia necesaria para la aplicaci?n.

    Primero asegura que el esquema de base de datos exista y
    despu?s carga datos iniciales idempotentes.
    """

    initialize_database()

    ensure_default_map_layers.execute()
    ensure_default_map_plans.execute()
    load_demo_physical_locations()
    load_demo_assets()


def _validate_foundation_registry() -> None:
    """
    Valida el registro estructural de Tenorio3G durante el arranque.

    Si existe una inconsistencia cr?tica, la aplicaci?n no debe
    iniciar silenciosamente.
    """

    RegistryValidator().validate()


def _register_blueprints(app: Flask) -> None:
    """
    Registra los m?dulos disponibles en la aplicaci?n.

    El orden sigue la jerarqu?a general de la plataforma:

    1. Core
    2. Foundation
    3. M?dulos funcionales
    """

    blueprints = (
        core,
        foundation,
        assets,
        maps,
        identity,
        work_orders,
        operations,
    )

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
