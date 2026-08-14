import os
from pathlib import Path


# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """
    Configuración base de Tenorio3G Platform.

    Todas las configuraciones específicas (desarrollo,
    pruebas y producción) heredan de esta clase.
    """

    # ==================================================
    # Flask
    # ==================================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "tenorio3g-foundation-2026"
    )
    
    # ==================================================
    # Aplicación
    # ==================================================

    APP_NAME = "Tenorio3G Platform"
    APP_VERSION = "0.2.0"

    # ==================================================
    # Rutas del proyecto
    # ==================================================

    BASE_DIR = BASE_DIR

    STORAGE_DIR = BASE_DIR / "storage"

    UPLOADS_DIR = STORAGE_DIR / "uploads"

    ASSETS_DIR = UPLOADS_DIR / "assets"

    ASSET_PHOTOS_DIR = ASSETS_DIR / "photos"

    ASSET_DOCUMENTS_DIR = ASSETS_DIR / "documents"

    EXPORTS_DIR = STORAGE_DIR / "exports"

    LOGS_DIR = STORAGE_DIR / "logs"

    # ==================================================
    # Flask
    # ==================================================

    DEBUG = False

    TESTING = False


class DevelopmentConfig(Config):

    DEBUG = True


class TestingConfig(Config):

    TESTING = True


class ProductionConfig(Config):

    DEBUG = False