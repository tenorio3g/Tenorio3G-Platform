from app.domains.assets.technical_data.repositories.technical_data_repository import (
    TechnicalDataRepository,
)

from .query import GetTechnicalDataQuery
from .result import GetTechnicalDataResult


class GetTechnicalData:
    """
    Obtiene la información técnica asociada a un activo.
    """

    def __init__(
        self,
        repository: TechnicalDataRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: GetTechnicalDataQuery,
    ) -> GetTechnicalDataResult:

        asset_code = query.asset_code.strip()

        if not asset_code:
            return GetTechnicalDataResult(
                success=False,
                message="El código del activo es obligatorio.",
            )

        technical_data = self._repository.get_by_asset_code(
            asset_code,
        )

        if technical_data is None:
            return GetTechnicalDataResult(
                success=False,
                message=(
                    "No existe información técnica "
                    "para este activo."
                ),
            )

        return GetTechnicalDataResult(
            success=True,
            message="Información técnica obtenida correctamente.",
            technical_data=technical_data,
        )