from app.domains.assets.technical_data.entities.technical_data import (
    TechnicalData,
)
from app.domains.assets.technical_data.repositories.technical_data_repository import (
    TechnicalDataRepository,
)


class InMemoryTechnicalDataRepository(
    TechnicalDataRepository,
):
    def __init__(self) -> None:
        self._items: dict[str, TechnicalData] = {}

    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> TechnicalData | None:
        return self._items.get(asset_code.strip())

    def save(
        self,
        technical_data: TechnicalData,
    ) -> None:
        self._items[technical_data.asset_code] = technical_data