from level import Level
from search import depth_first_search, expand


def test_expand_on_elevator():
    level = Level()
    level._load('level1.txt')
    start_node = (12, 3)  # row, col
    expanded_nodes, _ = expand(level._layout, start_node, '█')
    assert (len(expanded_nodes) == 2 and (13, 3) in expanded_nodes and (12, 4) in expanded_nodes)


def test_depth_first_search_on_elevator():
    level = Level()
    level._load('level1.txt')
    locations, _ = depth_first_search(level._layout, 13, 3, '█')
    assert ((12, 5) in locations and (14, 10) in locations)
