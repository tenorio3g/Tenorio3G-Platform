from app.domains.assets.spare_parts.repositories import (
    SQLiteSparePartRepository,
)

from app.domains.assets.spare_parts.use_cases.get_spare_parts_by_asset import (
    GetSparePartsByAsset,
)

from app.domains.assets.spare_parts.use_cases.save_spare_part import (
    SaveSparePart,
)


spare_part_repository = SQLiteSparePartRepository()

get_spare_parts_by_asset = GetSparePartsByAsset(
    spare_part_repository,
)

save_spare_part = SaveSparePart(
    spare_part_repository,
)