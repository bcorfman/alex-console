from game.chartypes import ROOM_CHARS
from game.level import Level
from game.search import graph_search, exhaustive_search, HallwayConstructionProblem, BlueprintSearchProblem
from game.util import LEVEL1, Queue, Node


def test_single_node_expansion_on_elevator():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = Node([12, 4])  # row, col
    problem = HallwayConstructionProblem(level.layout, start_node, ROOM_CHARS)
    expanded_nodes = problem.getSuccessors(start_node)
    assert len(expanded_nodes) == 2 and (13, 4) in expanded_nodes and (12, 5) in expanded_nodes


def test_room_construction_with_elevator():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = Node([13, 4])
    problem = HallwayConstructionProblem(level.layout, start_node, ROOM_CHARS)
    exhaustive_search(problem)
    assert (12, 6) in problem.visited and (14, 11) in problem.visited


def test_blueprint_problem_in_hallways():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = Node([5, 4])
    goal_node = Node([10, 56])
    bfs_problem = BlueprintSearchProblem(level.layout, start_node, goal_node)
    graph_search(bfs_problem, Queue())
    assert len(bfs_problem.actions) == 57  # between BFS and DFS, BFS gives shortest path
