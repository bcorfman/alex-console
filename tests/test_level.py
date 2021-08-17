from game.chartypes import ROOM_CHAR
from game.level import Level, Perimeter
from game.util import node_ordering, LEVEL1
from game.search import exhaustive_search, HallwayConstructionProblem, Node


def test_load_layout():
    level = Level()
    level._load_layout(LEVEL1)
    assert (level.layout[1][17] == 'C')


def test_load_layout_and_add_border():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    assert (level.layout[2][18] == 'C')


def test_location_ordering():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_loc = (12, 2)
    problem = HallwayConstructionProblem(level.layout, Node(start_loc), ROOM_CHAR)
    exhaustive_search(problem)
    assert ((12, 1) == min(problem.visited, key=node_ordering))
    assert ((14, 8) == max(problem.visited, key=node_ordering))


def test_find_room_name():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    p = Perimeter(Node([1, 9]), Node([3, 32]))
    assert p.find_room_name(level.layout) == 'CARGO'


def test_find_elevators():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    level._find_elevators()
    elevator1, elevator2 = level.elevators[0], level.elevators[1]
    assert (elevator1.name == 'ELEVATOR' and elevator1.perimeter.top_left == Node([1, 44]) and
            elevator1.perimeter.bottom_right == Node([3, 51]))
    assert (elevator2.name == 'ELEVATOR' and elevator2.perimeter.top_left == Node([12, 1]) and
            elevator2.perimeter.bottom_right == Node([14, 8]))


def test_initialize_level():
    level = Level(LEVEL1)
    assert len(level.rooms) == 3 and len(level.elevators) == 2


def test_hallways():
    level = Level(LEVEL1)
    assert len(level.hallways) == 17
    assert frozenset([(2, i) for i in range(33, 40)]) in level.hallways
    assert frozenset([(2, 40)]) in level.hallways
    assert frozenset([(2, i) for i in range(41, 44)])
    assert frozenset([(i, 40) for i in range(3, 10)]) in level.hallways
    assert frozenset([(10, 40)]) in level.hallways
    assert frozenset([(10, i) for i in range(36, 40)]) in level.hallways
    assert frozenset([(13, i) for i in range(9, 13)])
    assert frozenset([(13, 12)]) in level.hallways
    assert frozenset([(i, 12) for i in range(11, 13)]) in level.hallways
    assert frozenset([(10, 12)]) in level.hallways
    assert frozenset([(i, 12) for i in range(8, 10)]) in level.hallways
    assert frozenset([(10, i) for i in range(13, 18)]) in level.hallways
    assert frozenset([(10, i) for i in range(2, 12)]) in level.hallways
    assert frozenset([(10, 1)]) in level.hallways
    assert frozenset([(i, 1) for i in range(3, 10)]) in level.hallways
    assert frozenset([(2, 1)]) in level.hallways
    assert frozenset([(2, i) for i in range(2, 9)]) in level.hallways
