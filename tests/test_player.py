# noinspection PyPackageRequirements
import pytest
from game.player import Player
from game.level import Level
from game.util import LEVEL1, Loc


@pytest.mark.asyncio
async def test_player_move_to():
    level = Level(LEVEL1)
    vel = 2
    loc = level.rooms[0].exits[0]
    player = Player(name='Brandon', location=loc, parent=level, velocity=vel)
    goal = level.rooms[1].exits[0]
    await player.moveTo(goal)
    assert (list(player.actions) == [(2, i) for i in range(7, 1, -1)] +
            [(i, 1) for i in range(2, 10)] +
            [(10, i) for i in range(1, 18)])


@pytest.mark.asyncio
async def test_player_update():
    level = Level(LEVEL1)
    row, col = level.rooms[0].exits[0]
    start_loc = Loc(row, col)
    updated_loc = Loc(row, col - 1)
    player = Player(name='Brandon', location=start_loc, parent=level, velocity=2)
    player.numGameTicks = player.game_ticks_before_each_move + 1
    await player.moveTo(Loc(start_loc.row, start_loc.col - 2))
    player.update()
    assert (player.priorLocation == start_loc)
    assert (player.location == updated_loc)
