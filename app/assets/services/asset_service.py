from __future__ import annotations

from app.assets.presenters import AssetPresenter

from app.domains.assets.bootstrap import (
    find_all_assets,
)

from app.domains.assets.use_cases.find_all_assets.query import (
    FindAllAssetsQuery,
)


class AssetService:
    """
    Servicio de aplicación del módulo Assets.
    """

    @staticmethod
    def get_assets():

        result = find_all_assets.execute(
            FindAllAssetsQuery()
        )

        return [
            AssetPresenter.present(asset)
            for asset in result.assets
        ]