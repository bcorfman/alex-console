from game.level import Level
from game.util import LEVEL1, Loc


def test_elevator_exits():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    level._find_elevators()
    elevator1 = level.elevators[0]
    elevator2 = level.elevators[1]
    assert len(elevator1.exits) == 1 and len(elevator2.exits) == 1


def test_find_rooms():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    level._find_elevators()
    level._find_rooms()
    assert any(r for r in level.rooms if r.name == 'CARGO' and len(r.exits) == 2)


def test_player_not_contained_in_room():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    level._find_players()
    level._find_elevators()
    level._find_rooms()
    # players on the initial level are in hallways, not in rooms.
    player = level.get_first_player()
    player_in_room = False
    for room in level.rooms:
        if room.contains(player):
            player_in_room = True
            break
    assert not player_in_room


def test_player_contained_in_room():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    level._find_players()
    level._find_elevators()
    level._find_rooms()
    player = level.get_first_player()
    # move player's location to the top left corner of the first room.
    row, col = level.rooms[0].perimeter.top_left.state
    player.location = Loc(row, col)
    player_in_room = False
    for room in level.rooms:
        if room.contains(player):
            player_in_room = True
            break
    assert player_in_room
