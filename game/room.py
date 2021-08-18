from dataclasses import dataclass, field
from .util import Perimeter
from .player import Player


@dataclass
class Room:
    name: str
    perimeter: Perimeter
    exits: list[tuple] = field(default_factory=list)

    def contains(self, player: Player):
        tl_row, tl_col = self.perimeter.top_left.state
        br_row, br_col = self.perimeter.bottom_right.state
        return tl_col <= player.location.col <= br_col and tl_row <= player.location.row <= br_row
