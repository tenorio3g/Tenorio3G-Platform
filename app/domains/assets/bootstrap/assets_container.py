from __future__ import annotations

# ==========================================================
# Database
# ==========================================================

from app.foundation.database import SessionLocal

# ==========================================================
# Repositories
# ==========================================================

from app.domains.assets.repositories import (
    SQLiteAssetModelRepository,
    SQLiteAssetRepository,
)

# ==========================================================
# Seeder
# ==========================================================

from .demo_asset_seeder import DemoAssetSeeder

# ==========================================================
# Asset use cases
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

from app.domains.locations.bootstrap.locations_container import (
    repository as physical_location_repository,
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

# ==========================================================
# AssetModel use cases
# ==========================================================

from app.domains.assets.use_cases.find_all_asset_models.find_all_asset_models import (
    FindAllAssetModels,
)

from app.domains.assets.use_cases.find_asset_model_by_code.find_asset_model_by_code import (
    FindAssetModelByCode,
)

from app.domains.assets.use_cases.register_asset_model.register_asset_model import (
    RegisterAssetModel,
)

# ==========================================================
# Composite use cases
# ==========================================================

from app.domains.assets.use_cases.get_asset_life_sheet.get_asset_life_sheet import (
    GetAssetLifeSheet,
)

# ==========================================================
# Domain repositories
# ==========================================================

repository = SQLiteAssetRepository(
    SessionLocal
)

asset_model_repository = SQLiteAssetModelRepository(
    SessionLocal
)

# ==========================================================
# Initial demo data
# ==========================================================


def load_demo_assets() -> None:
    DemoAssetSeeder.load(
        asset_repository=repository,
        asset_model_repository=asset_model_repository,
    )


# ==========================================================
# Available Asset use cases
# ==========================================================

find_all_assets = FindAllAssets(
    repository,
)

find_asset_by_code = FindAssetByCode(
    repository,
)

register_asset = RegisterAsset(
    repository,
    asset_model_repository,
    physical_location_repository,
)

update_asset = UpdateAsset(
    repository,
    asset_model_repository,
    physical_location_repository,
)

activate_asset = ActivateAsset(
    repository,
)

deactivate_asset = DeactivateAsset(
    repository,
)

# ==========================================================
# Available AssetModel use cases
# ==========================================================

find_all_asset_models = FindAllAssetModels(
    asset_model_repository,
)

find_asset_model_by_code = FindAssetModelByCode(
    asset_model_repository,
)

register_asset_model = RegisterAssetModel(
    asset_model_repository,
)

# ==========================================================
# Composite use cases
# ==========================================================

get_asset_life_sheet = GetAssetLifeSheet(
    find_asset_by_code=find_asset_by_code,
    find_asset_model_by_code=find_asset_model_by_code,
)
