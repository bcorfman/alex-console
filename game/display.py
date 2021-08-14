from blessed import Terminal
from .level import Level
from .chartypes import ROOM_CHAR, HALLWAY_CHAR, PLAYER_CHARS


class Console:
    def __init__(self, level: Level, terminal: Terminal):
        self.term = terminal
        self.level = level
        self.t = 0

    def display(self):
        print(self.term.clear, end='', flush=True)
        for r, row in enumerate(self.level.layout):
            for c, col in enumerate(row):
                self.term.location(c, r)  # i.e. location(x, y)
                ch = self.level.layout[r][c]
                if ch == ROOM_CHAR:
                    print(self.term.tan_reverse(' '), end='', flush=True)
                elif ch == HALLWAY_CHAR:
                    print(self.term.white_reverse(' '), end='', flush=True)
                elif ch in PLAYER_CHARS:
                    print(self.term.white_reverse('\u26AB'), end='', flush=True)
                else:
                    print(ch, end='', flush=True)
        return True

    def update(self, row, col, left_button_pressed):
        if left_button_pressed:
            # move players according to actions
            count = str(self.t)
            length = len(count)
            print(self.term.move_xy(col, row) + count + self.term.move_left(length), end='', flush=True)
            self.t += 1
        return True
