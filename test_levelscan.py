from levelscan import load_layout, find_elevators, depth_first_search, expand, location_ordering


def test_load_layout():
    layout = load_layout('level1.txt')
    assert (layout[1][30] == 'C')


def test_expand():
    layout = load_layout('level1.txt')
    start_node = (11, 3)  # row, col
    expanded_nodes = expand(layout, start_node, '█')
    assert (len(expanded_nodes) == 2 and (12, 3) in expanded_nodes and (11, 4) in expanded_nodes)


def test_depth_first_search():
    layout = load_layout('level1.txt')
    locations = depth_first_search(layout, 12, 3, '█')
    assert ((11, 5) in locations and (13, 10) in locations)


def test_location_ordering():
    layout = load_layout('level1.txt')
    locations = depth_first_search(layout, 12, 3, '█')
    assert ((11, 3) == min(locations, key=location_ordering))
    assert ((13, 10) == max(locations, key=location_ordering))


def test_find_elevators():
    layout = load_layout('level1.txt')
    rooms = find_elevators(layout)
    assert (rooms[0].name == 'ELEVATOR' and rooms[0].top_left == (0, 61) and rooms[0].bottom_right == (2, 68))
    assert (rooms[1].name == 'ELEVATOR' and rooms[1].top_left == (11, 3) and rooms[1].bottom_right == (13, 10))
