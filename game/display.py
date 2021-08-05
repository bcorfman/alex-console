from .chartypes import ROOM_CHAR, HALLWAY_CHAR, PLAYER_CHARS


class Console:
    def __init__(self, level, terminal):
        self.term = terminal
        self.level = level
        self.t = 0
        self.display()

    def display(self):
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
                    print(self.term.white_reverse('\u26AB'), end='')
                else:
                    print(ch, end='')

    def update(self):
        print(self.term.home + str(self.t))
        self.t += 1
