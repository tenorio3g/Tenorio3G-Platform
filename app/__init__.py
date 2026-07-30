from flask import Flask

from config.config import Config

from app.assets import assets
from app.core.routes import core
from app.foundation import foundation
from app.foundation.registry import RegistryValidator
from app.operations import operations
from app.work_orders import work_orders


def create_app(config_class=Config) -> Flask:
    """
    Crea y configura la aplicación Flask de Tenorio3G.

    Args:
        config_class:
            Clase de configuración que será cargada por Flask.
            Permite utilizar configuraciones diferentes para
            desarrollo, pruebas y producción.

    Returns:
        Aplicación Flask completamente configurada.
    """

    app = Flask(__name__)

    app.config.from_object(config_class)

    _validate_foundation_registry()
    _register_blueprints(app)

    return app


def _validate_foundation_registry() -> None:
    """
    Valida el registro estructural de Tenorio3G durante el arranque.

    Si existe una inconsistencia crítica, la aplicación no debe
    iniciar silenciosamente.
    """

    RegistryValidator().validate()


def _register_blueprints(app: Flask) -> None:
    """
    Registra los módulos disponibles en la aplicación.

    El orden sigue la jerarquía general de la plataforma:

    1. Core
    2. Foundation
    3. Módulos funcionales
    """

    blueprints = (
        core,
        foundation,
        assets,
        work_orders,
        operations,
    )

    for blueprint in blueprints:
        app.register_blueprint(blueprint)