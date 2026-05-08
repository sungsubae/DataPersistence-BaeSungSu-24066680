import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Sample:
    name: str
    type: str
    spec: str
    unit: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("name must not be empty")
        if not self.type.strip():
            raise ValueError("type must not be empty")
