# noinspection PyPackageRequirements
import asyncio
import pytest
from game.characters import Player
from game.level import Level
from game.util import Loc, GAME_TICKS_PER_SECOND, GAME_TICK
from main import LEVEL1


@pytest.mark.asyncio
async def test_player_move_to():
    level = Level(LEVEL1)
    vel = 2
    loc = level.rooms[0].exits[0]
    player = Player(name='Brandon', location=loc, parent=level, velocity=vel)
    goal = level.rooms[1].exits[0]
    await player.moveTo(goal)
    assert (player.actions == list(reversed([Loc(2, i) for i in range(7, 1, -1)] +
            [Loc(i, 1) for i in range(2, 10)] +
            [Loc(10, i) for i in range(1, 18)])))


@pytest.mark.asyncio
async def test_player_update():
    level = Level(LEVEL1)
    exit_row, exit_col = level.rooms[0].exits[0].row, level.rooms[0].exits[0].col
    start_loc = Loc(exit_row, exit_col)
    distance = 2  # cells
    updated_loc = Loc(exit_row, exit_col - distance)
    player_velocity = 5  # cells per second
    player = Player(name='Brandon', location=start_loc, parent=level, velocity=player_velocity)
    # begin moving instantly from current cell by setting numGameTicks to max value
    player.numGameTicks = player.game_ticks_before_each_move + 1
    await player.moveTo(Loc(start_loc.row, start_loc.col - distance - 1))
    for i in range(GAME_TICKS_PER_SECOND // player_velocity * distance):
        player.update()
        await asyncio.sleep(GAME_TICK)
    # see if we've moved the correct distance
    assert (player.location == updated_loc)
