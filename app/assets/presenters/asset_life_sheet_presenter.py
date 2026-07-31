from app.assets.presenters.asset_life_sheet_view_model import (
    AssetLifeSheetViewModel,
)


class AssetLifeSheetPresenter:

    def present(self, asset) -> AssetLifeSheetViewModel:
        ...