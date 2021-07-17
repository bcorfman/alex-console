from blessed import Terminal
from .chartypes import ROOM_CHAR, HALLWAY_CHAR


class Console:
    def __init__(self, level):
        self.term = Terminal()
        self.level = level

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
                else:
                    print(ch, end='')

        print(self.term.home + f'({self.term.width}x{self.term.height})')
        print(self.term.move_down(20))


if __name__ == '__main__':
    from .level import Level

    level1 = Level(r'levels\level1.txt')
    console = Console(level1)
    console.display()
