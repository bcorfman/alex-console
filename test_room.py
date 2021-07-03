from level import Level


def test_elevator_exits():
    level = Level()
    level._load('level1.txt')
    level._find_elevators()
    elevator1 = level.elevators[0]
    elevator2 = level.elevators[1]
    assert len(elevator1.exits) == 1 and len(elevator2.exits) == 1


def test_find_rooms():
    level = Level()
    level._load('level1.txt')
    level._find_elevators()
    level._find_rooms()
    assert any(r for r in level.rooms if r.name == 'CARGO' and len(r.exits) == 2)
