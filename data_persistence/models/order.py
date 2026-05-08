import uuid
from dataclasses import dataclass, field
from datetime import datetime

VALID_STATUSES = {"PENDING", "PROCESSING", "COMPLETED", "CANCELLED"}


@dataclass
class Order:
    customer_name: str
    sample_id: str
    quantity: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "PENDING"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError(f"quantity must be positive, got {self.quantity}")
        if self.status not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}, got '{self.status}'")
