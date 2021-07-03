from level import Level, Perimeter
from util import location_ordering
from search import depth_first_search


def test_load_layout():
    level = Level()
    level._load('level1.txt')
    assert (level._layout[2][30] == 'C')


def test_location_ordering():
    level = Level()
    level._load('level1.txt')
    locations, _ = depth_first_search(level._layout, 13, 3, '█')
    assert ((12, 3) == min(locations, key=location_ordering))
    assert ((14, 10) == max(locations, key=location_ordering))


def test_find_room_name():
    level = Level()
    level._load('level1.txt')
    p = Perimeter((1, 16), (3, 49))
    assert p.find_room_name(level._layout) == 'CARGO'


def test_find_elevators():
    level = Level()
    level._load('level1.txt')
    level._find_elevators()
    elevator1, elevator2 = level.elevators[0], level.elevators[1]
    assert (elevator1.name == 'ELEVATOR' and elevator1.perimeter.top_left == (1, 61) and
            elevator1.perimeter.bottom_right == (3, 68))
    assert (elevator2.name == 'ELEVATOR' and elevator2.perimeter.top_left == (12, 3) and
            elevator2.perimeter.bottom_right == (14, 10))
