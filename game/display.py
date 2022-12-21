from itertools import chain

from .blueprint import Hallway, Room
from .characters import Player
from .level import Level
from .util import Loc, term


class Console:
    def __init__(self, level: Level):
        self.level = level
        self.t = 0

    def _print_avatar(self, player):
        output = None
        for obj in chain(self.level.rooms, self.level.elevators, self.level.hallways):
            if player in obj:
                output = obj.color + player.displayChar
                break
        with term.location(player.location.col, player.location.row):
            print(output, end="", flush=True)

    def _print_map_location(self, loc):
        row, col = loc.row, loc.col
        level_char = self.level.layout[row][col]
        output = ""
        for cls in [Hallway, Room, Player]:
            if level_char == cls.mapChar:
                output = self.level.translate_char(row, col)
                break
        else:
            output = term.white + level_char
        with term.location(col, row):  # i.e. location(x, y)
            print(output, end="", flush=True)

    def display(self):
        print(term.clear, end="", flush=True)
        for r, row in enumerate(self.level.layout):
            for c, col in enumerate(row):
                self._print_map_location(Loc(r, c))
        return True

    def update(self):
        for player in self.level.players:
            if (
                player.priorLocation is not None
                and player.location != player.priorLocation
            ):
                self._print_map_location(player.priorLocation)

            self._print_avatar(player)
