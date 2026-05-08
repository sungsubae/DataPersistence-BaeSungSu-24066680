from ..models.sample import Sample
from ..storage.json_storage import JsonStorage
from .base_repository import JsonRepository


class SampleRepository(JsonRepository[Sample]):
    def __init__(self, storage: JsonStorage):
        super().__init__(storage, Sample)
