from level import Level
from search import depth_first_search, BlueprintSearchProblem
from util import ROOM_CHAR


def test_expand_on_elevator():
    level = Level()
    level._load_layout('level1.txt')
    level._add_border_to_layout()
    start_node = (12, 4)  # row, col
    problem = BlueprintSearchProblem(level._layout, start_node, ROOM_CHAR)
    results = problem.getSuccessors(start_node)
    expanded_nodes = results.nodes
    assert len(expanded_nodes) == 2 and (13, 4) in expanded_nodes and (12, 5) in expanded_nodes


def test_depth_first_search_on_elevator():
    level = Level()
    level._load_layout('level1.txt')
    level._add_border_to_layout()
    start_node = (13, 4)
    problem = BlueprintSearchProblem(level._layout, start_node, ROOM_CHAR)
    results = depth_first_search(problem)
    assert (12, 6) in results.visited and (14, 11) in results.visited
