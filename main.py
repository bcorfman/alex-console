import asyncio
import curses
import os
import signal

from game.display import Console
from game.level import Level, Loc
from game.util import GAME_TICK, term

LEVEL1 = os.path.join(os.path.dirname(__file__), 'levels', 'level1.txt')


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


class ALEX:
    def __init__(self):
        self.level = Level(LEVEL1)
        self.console = Console(self.level)
        self.selected_player = self.level.get_first_player()

    def resize_event(self, _sig, _frame):
        self.console.display()

    async def game_loop(self, scr):
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGWINCH, self.resize_event, signal.SIGWINCH, None)
        self.console.display()
        scr.refresh()
        while True:
            c = scr.getch()
            if c == curses.KEY_MOUSE:
                _, col, row, _, _ = curses.getmouse()
                cursor_loc = Loc(row, col)
                player = self.level.check_for_player(cursor_loc)
                if player:
                    self.selected_player = player
                else:
                    if self.selected_player and self.level.is_valid_map_location(cursor_loc):
                        await self.selected_player.moveTo(cursor_loc)
                print(term.move_xy(col, row), end='', flush=True)  # moves cursor
            elif c == ord('q'):
                break
            await self.level.update()
            self.console.update()
            await asyncio.sleep(GAME_TICK)


async def main():
    # logging.basicConfig(filename='debug.txt', filemode='w', encoding='utf-8', level=logging.DEBUG)
    with LeftButtonPressed() as scr:
        alex = ALEX()
        await alex.game_loop(scr)


if __name__ == '__main__':
    asyncio.run(main())
