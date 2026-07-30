from app.assets.repositories.asset_repository import AssetRepository
from app.work_orders.repositories.work_order_repository import (
    WorkOrderRepository
)


class WorkOrderService:

    def __init__(self):

        self.repository = WorkOrderRepository()

    def obtener_orden(self, numero):

        return self.repository.obtener_por_numero(numero)