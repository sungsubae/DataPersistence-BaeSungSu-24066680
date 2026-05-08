from dataclasses import asdict
from typing import Generic, Optional, Type, TypeVar

from ..interfaces.repository import IRepository
from ..storage.json_storage import JsonStorage

T = TypeVar("T")


class JsonRepository(IRepository[T], Generic[T]):
    def __init__(self, storage: JsonStorage, model_class: Type[T], id_field: str = "id"):
        self._storage = storage
        self._model_class = model_class
        self._id_field = id_field

    def _from_dict(self, data: dict) -> T:
        return self._model_class(**data)

    def create(self, entity: T) -> T:
        records = self._storage.read_all()
        records.append(asdict(entity))
        self._storage.write_all(records)
        return entity

    def read(self, entity_id: str) -> Optional[T]:
        for record in self._storage.read_all():
            if record.get(self._id_field) == entity_id:
                return self._from_dict(record)
        return None

    def update(self, entity: T) -> T:
        records = self._storage.read_all()
        entity_id = getattr(entity, self._id_field)
        for i, record in enumerate(records):
            if record.get(self._id_field) == entity_id:
                records[i] = asdict(entity)
                self._storage.write_all(records)
                return entity
        raise KeyError(f"{self._model_class.__name__} with id '{entity_id}' not found")

    def delete(self, entity_id: str) -> bool:
        records = self._storage.read_all()
        filtered = [r for r in records if r.get(self._id_field) != entity_id]
        if len(filtered) == len(records):
            return False
        self._storage.write_all(filtered)
        return True

    def list_all(self) -> list[T]:
        return [self._from_dict(r) for r in self._storage.read_all()]
