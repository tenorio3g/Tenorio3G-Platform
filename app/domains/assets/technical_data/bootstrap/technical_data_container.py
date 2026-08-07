from app.domains.assets.technical_data.repositories.sqlite_technical_data_repository import (
    SQLiteTechnicalDataRepository,
)

from app.domains.assets.technical_data.use_cases.get_technical_data import (
    GetTechnicalData,
)

from app.domains.assets.technical_data.use_cases.save_technical_data import (
    SaveTechnicalData,
)

technical_data_repository = SQLiteTechnicalDataRepository()

get_technical_data = GetTechnicalData(
    technical_data_repository,
)

from app.domains.assets.technical_data.repositories.sqlite_technical_data_repository import (
    SQLiteTechnicalDataRepository,
)
from app.domains.assets.technical_data.use_cases.get_technical_data import (
    GetTechnicalData,
)
from app.domains.assets.technical_data.use_cases.save_technical_data import (
    SaveTechnicalData,
)


technical_data_repository = SQLiteTechnicalDataRepository()

get_technical_data = GetTechnicalData(
    technical_data_repository,
)

save_technical_data = SaveTechnicalData(
    technical_data_repository,
)