from dataclasses import dataclass, field
from util import Perimeter


@dataclass
class Room:
    name: str
    perimeter: Perimeter
    exits: list[tuple] = field(default_factory=list)
