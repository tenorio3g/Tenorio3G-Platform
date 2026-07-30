from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(slots=True)
class UpdateAssetModelCommand:

    code: str

    name: str

    description: str

    specifications: Mapping[str, str]