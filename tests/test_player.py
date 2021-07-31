from game.player import Player
from game.level import Level
from game.util import LEVEL1


def test_player():
    level = Level(LEVEL1)
    vel = 2
    loc = level.rooms[0].exits[0]
    player = Player('Brandon', vel, loc, level)
    goal = level.rooms[1].exits[0]
    assert (player.moveTo(goal) == [(10, i) for i in range(22, 4, -1)] +
            [(i, 4) for i in range(10, 2, -1)] + [(2, i) for i in range(4, 17)])
