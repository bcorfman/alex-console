from game.hallway import Hallway
from game.util import Loc


def test_hallway_creation_from_list():
    h = Hallway.from_list([Loc(2, 3), Loc(2, 4), Loc(2, 5)])
    assert (2, 3) in h
    assert Loc(2, 4) in h
