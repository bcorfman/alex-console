import asyncio
import curses
from concurrent.futures import ProcessPoolExecutor
from blessed import Terminal
from game.util import LEVEL1
from game.level import Level
from game.display import Console
from game.search import BlueprintSearchProblem, graph_search

GAME_TICKS_PER_SECOND = 20
GAME_TICK = 1.0 / GAME_TICKS_PER_SECOND


class LeftButtonPressed:
    def __init__(self):
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.scr.nodelay(True)
        self.scr.keypad(True)
        curses.mousemask(curses.BUTTON1_PRESSED)
        self.scr.refresh()  # TRICKY: without a refresh here, then the first getch() call will erase the screen

    def __enter__(self):
        return self.scr

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.nocbreak()
        self.scr.keypad(False)
        self.scr.nodelay(False)
        curses.echo()
        curses.endwin()


class Game:
    def __init__(self):
        self.term = Terminal()
        self.console = Console(Level(LEVEL1), self.term)

    async def event_loop(self, scr):
        row, col = None, None
        self.console.display()
        while True:
            pressed = False
            c = scr.getch()
            if c == self.term.KEY_MOUSE:
                pressed = True
                _, col, row, _, _ = curses.getmouse()
            elif c == ord('q'):
                break
            await asyncio.sleep(GAME_TICK)
            self.console.update(row, col, pressed)


async def main():
    with LeftButtonPressed() as scr:
        game = Game()
        await game.event_loop(scr)


if __name__ == '__main__':
    asyncio.run(main())
