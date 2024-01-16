from dataclasses import dataclass, field

from .characters import Player
from .util import Loc, term

IMAP = {
    'a1': 5,
    'c1': 6,
    'e1': 7,
    'g1': 8,
    'b2': 10,
    'd2': 11,
    'f2': 12,
    'h2': 13,
    'a3': 14,
    'c3': 15,
    'e3': 16,
    'g3': 17,
    'b4': 19,
    'd4': 20,
    'f4': 21,
    'h4': 22,
    'a5': 23,
    'c5': 24,
    'e5': 25,
    'g5': 26,
    'b6': 28,
    'd6': 29,
    'f6': 30,
    'h6': 31,
    'a7': 32,
    'c7': 33,
    'e7': 34,
    'g7': 35,
    'b8': 37,
    'd8': 38,
    'f8': 39,
    'h8': 40
}


@dataclass(frozen=True)
class Perimeter:
    top_left: Loc
    bottom_right: Loc

    def expand_border(self, amt=1):
        tl_row, tl_col = self.top_left.row, self.top_left.col
        br_row, br_col = self.bottom_right.row, self.bottom_right.col
        return Perimeter(Loc(tl_row - amt, tl_col - amt), Loc(br_row + amt, br_col + amt))

    def find_room_name(self, layout):
        tl_row, tl_col = self.top_left.row, self.top_left.col
        br_row, br_col = self.bottom_right.row, self.bottom_right.col
        chars = []
        for r in range(tl_row, br_row + 1):
            for c in range(tl_col, br_col + 1):
                if layout[r][c] != Room.mapChar:
                    chars.append(layout[r][c])
        return "".join(chars).strip()


@dataclass
class Room:
    name: str
    perimeter: Perimeter
    exits: list[Loc] = field(default_factory=list)
    mapChar: str = "█"
    color: str = term.tan
    displayChar: str = term.reverse(" ")

    def __contains__(self, item):
        tl_row, tl_col = self.perimeter.top_left.row, self.perimeter.top_left.col
        br_row, br_col = (
            self.perimeter.bottom_right.row,
            self.perimeter.bottom_right.col,
        )
        if isinstance(item, Player):
            return (tl_col <= item.location.col <= br_col and tl_row <= item.location.row <= br_row)
        elif isinstance(item, Loc):
            return tl_col <= item.col <= br_col and tl_row <= item.row <= br_row
        else:
            raise TypeError("Unrecognized type for Room.__contains___()")


class Hallway:
    mapChar = "~"
    color = term.white
    displayChar = term.reverse(" ")

    def __init__(self, locations):
        self.locations = frozenset(locations)

    def __eq__(self, other):
        if isinstance(other, frozenset):
            return self.locations == other
        else:
            return self.locations == other.locations

    def __contains__(self, item):
        if isinstance(item, Player):
            return item.location in self.locations
        else:
            return item in self.locations

    def __hash__(self):
        return hash(self.locations)

    @classmethod
    def from_list(cls, lst):
        hallway = cls.__new__(cls)
        hallway.locations = frozenset(lst)
        return hallway
