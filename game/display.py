from threading import Timer
from blessed import Terminal
from .chartypes import ROOM_CHAR, HALLWAY_CHAR, PLAYER_CHARS
from util import GAME_TICK, LEVEL1


class Console:
    def __init__(self, level):
        self.term = Terminal()
        self.level = level
        self.timer = Timer(GAME_TICK, self._update)

    def _display(self):
        print(self.term.clear)
        for r, row in enumerate(self.level.layout):
            for c, col in enumerate(row):
                self.term.location(c, r)  # i.e. location(x, y)
                ch = self.level.layout[r][c]
                if ch == ROOM_CHAR:
                    print(self.term.tan_reverse(' '), end='')
                elif ch == HALLWAY_CHAR:
                    print(self.term.white_reverse(' '), end='')
                elif ch in PLAYER_CHARS:
                    print(self.term.white_reverse('\u26AB', end=''))
                else:
                    print(ch, end='')

        print(self.term.home + f'({self.term.width}x{self.term.height})')
        print(self.term.move_down(20))

    def _update(self):
        self.level.update()
        # wait for keyboard input, which may indicate
        # a new direction (up/down/left/right)
        inp = self.term.inkey(timeout=GAME_TICK / 2.0)

        print(inp.code)


# def next_bearing(term, inp_code, bearing):
#    """
#    Return direction function for new bearing by inp_code.
#    If no inp_code matches a bearing direction, return a function for the current bearing.
#    """
#    return {
#        term.KEY_LEFT: left_of,
#        term.KEY_RIGHT: right_of,
#        term.KEY_UP: above,
#        term.KEY_DOWN: below,
#    }.get(inp_code,
#          # direction function given the current bearing
#          {LEFT: left_of,
#           RIGHT: right_of,
#           UP: above,
#           DOWN: below}[(bearing.y, bearing.x)])


if __name__ == '__main__':
    from .level import Level

    level1 = Level(LEVEL1)
    console = Console(level1)
