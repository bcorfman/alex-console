from game.level import Level, Perimeter
from game.util import location_ordering, ROOM_CHAR, LEVEL1, Stack
from game.search import graph_search, BlueprintSearchProblem


def test_load_layout():
    level = Level()
    level._load_layout(LEVEL1)
    assert (level.layout[1][30] == 'C')


def test_load_layout_and_add_border():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    assert (level.layout[2][31] == 'C')


def test_location_ordering():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = (13, 4)
    problem = BlueprintSearchProblem(level.layout, start_node, ROOM_CHAR)
    results = graph_search(problem, Stack())
    assert ((12, 4) == min(results.visited, key=location_ordering))
    assert ((14, 11) == max(results.visited, key=location_ordering))


def test_find_room_name():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    p = Perimeter((1, 17), (3, 50))
    assert p.find_room_name(level.layout) == 'CARGO'


def test_find_elevators():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    level._find_elevators()
    elevator1, elevator2 = level.elevators[0], level.elevators[1]
    assert (elevator1.name == 'ELEVATOR' and elevator1.perimeter.top_left == (1, 62) and
            elevator1.perimeter.bottom_right == (3, 69))
    assert (elevator2.name == 'ELEVATOR' and elevator2.perimeter.top_left == (12, 4) and
            elevator2.perimeter.bottom_right == (14, 11))


def test_initialize_level():
    level = Level(LEVEL1)
    assert len(level.rooms) == 3 and len(level.elevators) == 2


def test_hallways():
    level = Level(LEVEL1)
    assert len(level.hallways) == 17
    assert frozenset([(2, i) for i in range(51, 57)]) in level.hallways
    assert frozenset([(2, 57)]) in level.hallways
    assert frozenset([(2, i) for i in range(58, 62)])
    assert frozenset([(i, 57) for i in range(3, 10)]) in level.hallways
    assert frozenset([(10, 57)]) in level.hallways
    assert frozenset([(10, i) for i in range(52, 57)]) in level.hallways
    assert frozenset([(13, i) for i in range(12, 16)])
    assert frozenset([(13, 16)]) in level.hallways
    assert frozenset([(i, 16) for i in range(11, 13)]) in level.hallways
    assert frozenset([(10, 16)]) in level.hallways
    assert frozenset([(i, 16) for i in range(8, 10)]) in level.hallways
    assert frozenset([(10, i) for i in range(17, 24)]) in level.hallways
    assert frozenset([(10, i) for i in range(5, 16)]) in level.hallways
    assert frozenset([(10, 4)]) in level.hallways
    assert frozenset([(i, 4) for i in range(3, 10)]) in level.hallways
    assert frozenset([(2, 4)]) in level.hallways
    assert frozenset([(2, i) for i in range(5, 17)]) in level.hallways
