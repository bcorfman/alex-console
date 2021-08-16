from game.agent import Player
from game.level import Level
from game.util import LEVEL1
import pytest


@pytest.mark.asyncio
async def test_player():
    level = Level(LEVEL1)
    vel = 2
    loc = level.rooms[0].exits[0]
    player = Player(name='Brandon', location=loc, parent=level, velocity=vel)
    goal = level.rooms[1].exits[0]
    await player.moveTo(goal)
    assert (player.actions == [(2, i) for i in range(7, 1, -1)] +
            [(i, 1) for i in range(2, 10)] +
            [(10, i) for i in range(1, 18)])
