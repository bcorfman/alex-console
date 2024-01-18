from abc import ABC, abstractmethod

from .util import Loc, Node, PriorityQueue, Queue, Stack, manhattan_distance


class SearchProblem(ABC):

    @abstractmethod
    def getStartNode(self):
        """Returns the start state for the search."""

    @abstractmethod
    def isGoal(self, node):
        """Returns True if _goal state is found; False otherwise."""

    @abstractmethod
    def getSuccessors(self, node):
        """Given a search node, the agent must make a one or more individual moves from that 
        state, and return them as a list of successors."""

    @abstractmethod
    def storeResults(self, node, visited, num_explored):
        """Once search is complete, use this method to store the results.
        Visited nodes are passed in directly from graph_search, while other data generated in
        getSuccessors should be stored as the problem is solved and stored during this method 
        call."""

    def getCostOfActions(self, actions):
        return len(actions)

    @abstractmethod
    def h(self, state):
        """Returns the heuristic value of a given state."""


class BlueprintSearchProblem(SearchProblem):

    def __init__(self, grid, start_node, goal_node):
        self._grid = grid
        self._start_node = start_node
        self._goal_node = goal_node
        self.actions = []
        self.num_visited = 0
        self.num_explored = 0

    def getStartNode(self):
        return self._start_node

    def isGoal(self, node):
        return node == self._goal_node

    def storeResults(self, node, visited, num_explored):
        self.actions = list(reversed(node.actions))
        self.num_visited = len(visited)
        self.num_explored = num_explored

    def applicable(self, loc):
        return self._grid[loc.row][loc.col] != " "

    def apply(self, node, loc):
        return Node(loc, node.actions + [loc], node.cost + 1)

    def getSuccessors(self, node):
        nodes = []
        src_row, src_col = node.state.row, node.state.col
        for offset_row, offset_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = src_row + offset_row, src_col + offset_col
            new_loc = Loc(new_row, new_col)
            if self.applicable(new_loc):
                new_node = self.apply(node, new_loc)
                nodes.append(new_node)
        return nodes

    def h(self, state):
        return manhattan_distance(self._goal_node.state, state)


class HallwayConstructionProblem(SearchProblem):

    def __init__(self, grid, start_node, search_char):
        self._grid = grid
        self.fringe = []
        self._start_node = start_node
        self._search_char = search_char
        self.hallways = set()
        self.rooms = []
        self._search_locations = set()
        self.room_entrances = set()
        self._goal = None
        self.visited = None
        self.num_explored = 0

    def getStartNode(self):
        return self._start_node

    def getSuccessors(self, node):
        from .blueprint import Hallway

        nodes = []
        src_row, src_col = node.state.row, node.state.col
        valid_offsets = []
        for offset_row, offset_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = src_row + offset_row, src_col + offset_col
            new_loc = Loc(new_row, new_col)
            if self._grid[new_row][new_col] == self._search_char:
                valid_offsets.append((offset_row, offset_col))
                nodes.append(Node(new_loc, node.actions + [new_loc], node.cost + 1))
            elif self._grid[new_row][new_col] != " ":
                self.fringe.append(new_loc)
        cross_junction = len(valid_offsets) == 4
        t_or_corner_junction = len(valid_offsets) > 1 and (sum(
            (row for row, _ in valid_offsets)) != 0 or sum((col for _, col in valid_offsets)) != 0)
        start_node = self.getStartNode()
        dead_end = len(valid_offsets) == 1 and start_node.state != (src_row, src_col)
        if cross_junction or t_or_corner_junction:
            self.hallways.add(Hallway(loc for loc in self._search_locations))
            self.hallways.add(Hallway((node.state, )))
            self._search_locations.clear()
        elif dead_end:
            self._search_locations.add(node.state)
            self.hallways.add(Hallway(loc for loc in self._search_locations))
            self._search_locations.clear()
        elif node == self.getStartNode() or not t_or_corner_junction:
            self._search_locations.add(node.state)
        else:
            raise ValueError("unrecognized junction type")
        return nodes

    def isGoal(self, node):
        # only use in AStarSearch
        return NotImplementedError

    def storeResults(self, node, visited, num_explored):
        self.visited = visited
        self.num_explored = num_explored
        for outlier in self.fringe:
            if outlier not in self.room_entrances:
                self.room_entrances.add(outlier)

    def h(self, state):
        # only use in AStarSearch
        return 0


def exhaustive_search(problem):
    """Search until all nodes have been expanded, then return results."""
    frontier = Stack()
    frontier.update(problem.getStartNode())
    visited = set()
    node = None
    num_explored = 0
    while not frontier.isEmpty():
        node = frontier.pop()
        num_explored += 1
        visited.add(node.state)
        successors = problem.getSuccessors(node)
        for new_node in successors:
            if new_node.state not in visited:
                frontier.update(new_node)
    problem.storeResults(node, visited, num_explored)


def graph_search(problem: SearchProblem, frontier):
    result = None
    initial_node = problem.getStartNode()
    initial_cost = problem.h(initial_node.state)
    frontier.update(initial_node, initial_cost)
    visited = set()
    num_explored = 0
    while not frontier.isEmpty():
        node = frontier.pop()
        num_explored += 1
        if problem.isGoal(node):
            problem.storeResults(node, visited, num_explored)
            result = problem
            break
        visited.add(node.state)
        for new_node in problem.getSuccessors(node):
            if new_node.state not in visited and new_node not in frontier:
                frontier.push(new_node, new_node.cost + problem.h(new_node.state))
            elif new_node in frontier:
                frontier.update(new_node, new_node.cost + problem.h(new_node.state))
    return result


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = Queue()
    return graph_search(problem, frontier)


def astar_search(problem):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = PriorityQueue()
    return graph_search(problem, frontier)
