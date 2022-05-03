from game.level import Level
from game.blueprint import Room
from game.search import breadth_first_search, astar_search, exhaustive_search, HallwayConstructionProblem, \
    BlueprintSearchProblem
from game.util import Node, Loc, PriorityQueue
from main import LEVEL1


def test_single_node_expansion_on_elevator():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = Node(Loc(12, 1))  # row, col
    problem = HallwayConstructionProblem(level.layout, start_node, Room.mapChar)
    expanded_nodes = problem.getSuccessors(start_node)
    assert len(expanded_nodes) == 2 and Node(Loc(12, 2)) in expanded_nodes and Node(Loc(13, 1)) in expanded_nodes


def test_room_construction_with_elevator():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = Node(Loc(13, 2))
    problem = HallwayConstructionProblem(level.layout, start_node, Room.mapChar)
    exhaustive_search(problem)
    assert Loc(12, 6) in problem.visited and Loc(14, 8) in problem.visited


def test_astar_search_initial_priority_with_blueprint():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = Node(Loc(5, 1))
    goal_node = Node(Loc(10, 40))
    astar_problem = BlueprintSearchProblem(level.layout, start_node, goal_node)
    frontier = PriorityQueue()
    for node in astar_problem.getSuccessors(start_node):
        frontier.push(node, node.cost)
    node = frontier.pop()
    assert node.state == Loc(6, 1)
    assert node.cost + astar_problem.h(node.state) == 1 + 43
    node = frontier.pop()
    assert node.state == Loc(4, 1)
    assert node.cost + astar_problem.h(node.state) == 1 + 45


def test_blueprint_problem_in_hallways():
    level = Level()
    level._load_layout(LEVEL1)
    level._add_border_to_layout()
    start_node = Node(Loc(10, 12))
    goal_node = Node(Loc(1, 51))
    bfs_problem = BlueprintSearchProblem(level.layout, start_node, goal_node)
    astar_problem = BlueprintSearchProblem(level.layout, start_node, goal_node)
    breadth_first_search(bfs_problem)
    astar_search(astar_problem)
    assert astar_problem.num_explored < bfs_problem.num_explored
    assert len(bfs_problem.actions) == 48
    assert len(astar_problem.actions) == 48
    start_node = Node(Loc(1, 51))
    goal_node = Node(Loc(8, 1))
    bfs_problem = BlueprintSearchProblem(level.layout, start_node, goal_node)
    astar_problem = BlueprintSearchProblem(level.layout, start_node, goal_node)
    breadth_first_search(bfs_problem)
    astar_search(astar_problem)
    assert astar_problem.num_explored < bfs_problem.num_explored
    assert len(bfs_problem.actions) == 57
    assert len(astar_problem.actions) == 57
