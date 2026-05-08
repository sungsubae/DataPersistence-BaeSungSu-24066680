from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    @abstractmethod
    def create(self, entity: T) -> T: ...

    @abstractmethod
    def read(self, entity_id: str) -> Optional[T]: ...

    @abstractmethod
    def update(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, entity_id: str) -> bool: ...

    @abstractmethod
    def list_all(self) -> list[T]: ...
