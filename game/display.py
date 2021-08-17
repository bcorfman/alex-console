import logging
from blessed import Terminal
from .level import Level
from .chartypes import ROOM_CHAR, HALLWAY_CHAR, PLAYER_AVATAR


class Console:
    def __init__(self, level: Level):
        self.term = Terminal()
        self.level = level
        self.t = 0

    def display(self):
        print(self.term.clear, end='', flush=True)
        for r, row in enumerate(self.level.layout):
            for c, col in enumerate(row):
                self.term.location(c, r)  # i.e. location(x, y)
                self._print_char(self.level.layout[r][c])
        return True

    def update(self):
        for player in self.level.players:
            if player.priorLocation is not None and player.location != player.priorLocation:
                # overwrite player's prior location with the original map layer
                r, c = player.priorLocation.row, player.priorLocation.col
                with self.term.location(c, r):  # i.e. location(x, y)
                    logging.debug(f'prior location: {r},{c}')
                    self._print_char(self.level.layout[r][c])
            # write at current location with the player character
            r, c = player.location.row, player.location.col
            with self.term.location(c, r):  # i.e. location(x, y)
                logging.debug(f'location: {r},{c}')
                self._print_char(player.avatar)

    def _print_char(self, ch):
        if ch == ROOM_CHAR:
            print(self.term.tan_reverse(' '), end='', flush=True)
        elif ch == HALLWAY_CHAR:
            print(self.term.white_reverse(' '), end='', flush=True)
        elif ch == PLAYER_AVATAR:
            print(self.term.white_reverse(ch), end='', flush=True)
        else:
            print(ch, end='', flush=True)
