from ..models.order import Order
from ..storage.json_storage import JsonStorage
from .base_repository import JsonRepository


class OrderRepository(JsonRepository[Order]):
    def __init__(self, storage: JsonStorage):
        super().__init__(storage, Order)
