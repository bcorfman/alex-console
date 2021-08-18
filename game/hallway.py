from dataclasses import dataclass
from .chartypes import HALLWAY_CHAR
from .util import Loc, term


@dataclass
class Hallway:
    locations: frozenset[Loc]
    mapChar: str = HALLWAY_CHAR
    displayChar: str = term.white_reverse(' ')
