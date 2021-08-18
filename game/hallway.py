from dataclasses import dataclass
from .chartypes import HALLWAY_CHAR
from .util import Loc, term


@dataclass
class Hallway:
    locations: frozenset[Loc]
    mapChar: str = HALLWAY_CHAR
    displayChar: str = term.white_reverse(' ')

    @classmethod
    def from_list(cls, lst):
        hallway = cls.__new__(cls)
        hallway.locations = frozenset(lst)
        return hallway
