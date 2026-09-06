from __future__ import annotations

from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)
from app.domains.locations.repositories.physical_location_repository import (
    PhysicalLocationRepository,
)


class DemoPhysicalLocationSeeder:

    @staticmethod
    def load(
        repository: PhysicalLocationRepository,
    ) -> None:

        location_code = "SUBESTACION-NORTE"

        if repository.find_by_code(
            location_code
        ) is not None:
            return

        repository.save(
            PhysicalLocation(
                code=location_code,
                name="Subestacion Norte",
                area="SERVICIOS",
            )
        )
