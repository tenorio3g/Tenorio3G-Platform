from __future__ import annotations

# ==========================================================
# Repositorio
# ==========================================================

from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
)

# ==========================================================
# Seeder
# ==========================================================

from .demo_asset_seeder import DemoAssetSeeder

# ==========================================================
# Casos de Uso
# ==========================================================

from app.domains.assets.use_cases.find_all_assets.find_all_assets import (
    FindAllAssets,
)

from app.domains.assets.use_cases.find_asset_by_code.find_asset_by_code import (
    FindAssetByCode,
)

from app.domains.assets.use_cases.register_asset.register_asset import (
    RegisterAsset,
)

from app.domains.assets.use_cases.update_asset.update_asset import (
    UpdateAsset,
)

from app.domains.assets.use_cases.activate_asset.activate_asset import (
    ActivateAsset,
)

from app.domains.assets.use_cases.deactivate_asset.deactivate_asset import (
    DeactivateAsset,
)

from app.domains.assets.repositories.in_memory_asset_model_repository import (
    InMemoryAssetModelRepository,
)
# ==========================================================
# Repositorio único del dominio
# ==========================================================

repository = InMemoryAssetRepository()
asset_model_repository = InMemoryAssetModelRepository()

# ==========================================================
# Datos Demo
# ==========================================================

DemoAssetSeeder.load(repository)

# ==========================================================
# Casos de uso disponibles
# ==========================================================

find_all_assets = FindAllAssets(repository)

find_asset_by_code = FindAssetByCode(repository)

register_asset = RegisterAsset(
    repository,
    asset_model_repository,
)

update_asset = UpdateAsset(repository)

activate_asset = ActivateAsset(repository)

deactivate_asset = DeactivateAsset(repository)