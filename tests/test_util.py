from game.util import Loc


def test_create_loc_from_tuple():
    loc = Loc.from_tuple((2, 8))
    assert loc.row == 2 and loc.col == 8


def test_loc_equals():
    assert Loc(2, 3) == Loc(2, 3)
    assert Loc(2, 3) == Loc.from_tuple((2, 3))
    assert Loc(2, 3) == (2, 3)
