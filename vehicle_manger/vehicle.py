from dataclasses import dataclass
from typing import Optional


@dataclass
class Vehicle:
    name: str
    model: str
    year: int
    color: str
    price: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    id: Optional[int] = None
