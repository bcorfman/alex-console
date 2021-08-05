import asyncio
from blessed import Terminal
from game.util import LEVEL1
from game.level import Level
from game.display import Console

GAME_TICKS_PER_SECOND = 20
GAME_TICK = 1.0 / GAME_TICKS_PER_SECOND


class Game:
    def __init__(self):
        self.term = Terminal()
        self.console = Console(Level(LEVEL1), self.term)
        self.loop = asyncio.get_event_loop()

    async def event_loop(self):
        with self.term.hidden_cursor(), self.term.cbreak():
            while True:
                key = self.term.inkey(timeout=0.00)
                if key.code == self.term.KEY_ESCAPE:
                    break
                await asyncio.sleep(GAME_TICK)
                self.console.update()
        self.term.move_yx(25, 0)


async def main():
    game = Game()
    await game.event_loop()


if __name__ == '__main__':
    asyncio.run(main())
