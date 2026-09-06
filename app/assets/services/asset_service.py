from __future__ import annotations

from app.assets.presenters import AssetPresenter

from app.domains.assets.bootstrap import (
    find_all_assets,
)
from app.domains.assets.use_cases.find_all_assets.query import (
    FindAllAssetsQuery,
)
from app.domains.locations.bootstrap.locations_container import (
    repository as physical_location_repository,
)


class AssetService:
    """
    Servicio de aplicacion del modulo Assets.
    """

    @staticmethod
    def get_assets():

        result = find_all_assets.execute(
            FindAllAssetsQuery()
        )

        activos = []

        for asset in result.assets:

            physical_location = (
                physical_location_repository.find_by_code(
                    asset.location_code
                )
            )

            activos.append(
                AssetPresenter.present(
                    asset,
                    physical_location=physical_location,
                )
            )

        return activos
