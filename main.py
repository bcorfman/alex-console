import asyncio
import curses
import logging
from game.util import LEVEL1, GAME_TICK
from game.level import Level, Loc
from game.display import Console


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
        self.level = Level(LEVEL1)
        self.console = Console(self.level)
        self.selected_player = self.level.get_first_player()

    async def event_loop(self, scr):
        self.console.display()
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
            elif c == ord('q'):
                break
            await self.level.update()
            self.console.update()
            await asyncio.sleep(GAME_TICK)


# noinspection PyArgumentList
async def main():
    logging.basicConfig(filename='debug.txt', filemode='w', encoding='utf-8', level=logging.DEBUG)
    with LeftButtonPressed() as scr:
        game = Game()
        await game.event_loop(scr)


if __name__ == '__main__':
    asyncio.run(main())
