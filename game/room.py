from dataclasses import dataclass, field
from .chartypes import ROOM_CHAR
from .util import Perimeter, term
from .player import Player


@dataclass
class Room:
    name: str
    perimeter: Perimeter
    exits: list[tuple] = field(default_factory=list)
    mapChar: str = ROOM_CHAR
    displayChar: str = term.tan_reverse(' ')

    def contains(self, player: Player):
        tl_row, tl_col = self.perimeter.top_left.state
        br_row, br_col = self.perimeter.bottom_right.state
        return tl_col <= player.location.col <= br_col and tl_row <= player.location.row <= br_row
