import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Inventory:
    sample_id: str
    quantity: int
    location: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError(f"quantity must not be negative, got {self.quantity}")
