from game.util import Loc, manhattan_distance, PriorityQueue


def test_create_loc_from_tuple():
    loc = Loc.from_tuple((2, 8))
    assert loc.row == 2 and loc.col == 8


def test_loc_equals():
    assert Loc(2, 3) == Loc(2, 3)
    assert Loc(2, 3) == Loc.from_tuple((2, 3))
    assert Loc(2, 3) == (2, 3)


def test_manhattan_distance():
    assert manhattan_distance(Loc(2, 3), Loc(4, 5)) == 4
    assert manhattan_distance(Loc(-2, 3), Loc(2, -5)) == 12


def test_priority_queue():
    pq = PriorityQueue()
    pq.push('a', 12)
    pq.push('b', 15)
    pq.push('c', 7)
    pq.update('b', 13)
    pq.update('a', 8)
    item = pq.pop()
    assert item == 'c'
    item = pq.pop()
    assert item == 'a'
    item = pq.pop()
    assert item == 'b'
