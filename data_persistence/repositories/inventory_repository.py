from ..models.inventory import Inventory
from ..storage.json_storage import JsonStorage
from .base_repository import JsonRepository


class InventoryRepository(JsonRepository[Inventory]):
    def __init__(self, storage: JsonStorage):
        super().__init__(storage, Inventory)
