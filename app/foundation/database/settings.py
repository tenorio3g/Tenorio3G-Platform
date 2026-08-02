"""
====================================================

Tenorio3G Platform

Foundation Database Settings

====================================================
"""

from pathlib import Path

# Raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Carpeta storage
STORAGE_PATH = PROJECT_ROOT / "storage"

# Crear carpeta automáticamente
STORAGE_PATH.mkdir(exist_ok=True)

# Archivo SQLite
DATABASE_PATH = STORAGE_PATH / "tenorio3g.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"