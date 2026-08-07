from abc import ABC
from abc import abstractmethod


class TechnicalDataRepository(ABC):

    @abstractmethod
    def get_by_asset_code(
        self,
        asset_code: str,
    ):
        pass


    @abstractmethod
    def save(
        self,
        technical_data,
    ):
        pass