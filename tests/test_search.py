from game.level import Level
from game.blueprint import Room
from game.search import astar_search, exhaustive_search, HallwayConstructionProblem, BlueprintSearchProblem
from game.util import Queue, Node, Loc
from main import LEVEL1


def test_single_node_expansion_on_elevator():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = Node(Loc(12, 1))  # row, col
    problem = HallwayConstructionProblem(level.layout, start_node, Room.mapChar)
    expanded_nodes = problem.getSuccessors(start_node)
    assert len(expanded_nodes) == 2 and (12, 2) in expanded_nodes and (13, 1) in expanded_nodes


def test_room_construction_with_elevator():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = Node(Loc(13, 2))
    problem = HallwayConstructionProblem(level.layout, start_node, Room.mapChar)
    exhaustive_search(problem)
    assert (12, 6) in problem.visited and (14, 8) in problem.visited


def test_blueprint_problem_in_hallways():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = Node(Loc(5, 1))
    goal_node = Node(Loc(10, 40))
    bfs_problem = BlueprintSearchProblem(level.layout, start_node, goal_node)
    astar_search(bfs_problem)
    assert len(bfs_problem.actions) == 44

