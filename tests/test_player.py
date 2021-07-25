from game.player import Player
from game.level import Level
from game.util import LEVEL1


def test_player():
    level = Level(LEVEL1)
    player = Player('Brandon', 2, level.rooms[0].exits[0])
    assert (player.moveTo(level.rooms[1].exits[0]))
