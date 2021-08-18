from game.util import Loc


def test_create_loc_from_tuple():
    loc = Loc.from_tuple((2, 8))
    assert loc.row == 2 and loc.col == 8
