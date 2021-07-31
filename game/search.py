from abc import ABC, abstractmethod
from .util import Stack, Node


class SearchProblem(ABC):
    @abstractmethod
    def getStartNode(self):
        """ Returns the start state for the search. """

    @abstractmethod
    def isGoal(self, node):
        """ Returns True if _goal state is found; False otherwise. """

    @abstractmethod
    def getSuccessors(self, node):
        """ Given a search node, the agent must make a one or more individual moves from that state,
          and return them as a list of successors. """

    @abstractmethod
    def storeResults(self, visited):
        """ Once search is complete, use this method to store the results.
        Visited nodes are passed in directly from graph_search, while other data generated in
        getSuccessors should be stored as the problem is solved and stored during this method call. """

    def getCostOfActions(self, actions):
        return len(actions)


class BlueprintSearchProblem(SearchProblem):
    def __init__(self, grid, start_node, goal_node):
        self._grid = grid
        self._start_node = start_node
        self._goal_node = goal_node
        self.actions = []

    def getStartNode(self):
        return self._start_node

    def isGoal(self, node):
        return node == self._goal_node

    def storeResults(self, node):
        self.actions = list(node.actions)

    def getSuccessors(self, node):
        nodes = []
        src_row, src_col = node.state
        for offset_row, offset_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_loc = new_row, new_col = src_row + offset_row, src_col + offset_col
            if self._grid[new_row][new_col] != ' ':
                nodes.append(Node(new_loc, node.actions + [new_loc], node.cost + 1))
        return nodes


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

    def getStartNode(self):
        return self._start_node

    def getSuccessors(self, node):
        nodes = []
        src_row, src_col = node.state
        valid_offsets = []
        for offset_row, offset_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_loc = new_row, new_col = src_row + offset_row, src_col + offset_col
            if self._grid[new_row][new_col] == self._search_char:
                valid_offsets.append((offset_row, offset_col))
                nodes.append(Node(new_loc, node.actions + [new_loc], node.cost + 1))
            elif self._grid[new_row][new_col] != ' ':
                self.fringe.append(new_loc)
        cross_junction = len(valid_offsets) == 4
        t_or_corner_junction = (len(valid_offsets) > 1 and
                                (sum([row for row, _ in valid_offsets]) != 0 or
                                 sum([col for _, col in valid_offsets]) != 0))
        start_node = self.getStartNode()
        dead_end = len(valid_offsets) == 1 and start_node.state != (src_row, src_col)
        if cross_junction or t_or_corner_junction:
            self.hallways.add(frozenset(self._search_locations))
            self.hallways.add(frozenset([node.state]))
            self._search_locations.clear()
        elif dead_end:
            self._search_locations.add(node.state)
            self.hallways.add(frozenset(self._search_locations))
            self._search_locations.clear()
        elif node == self.getStartNode() or not t_or_corner_junction:
            self._search_locations.add(node.state)
        else:
            raise ValueError('unrecognized junction type')
        return nodes

    def isGoal(self, node):
        return NotImplementedError

    def storeResults(self, visited_nodes):
        self.visited = visited_nodes
        for outlier in self.fringe:
            if outlier not in self.room_entrances:
                self.room_entrances.add(outlier)


def exhaustive_search(problem):
    """ Search until all nodes have been expanded, then return results. """
    frontier = Stack()
    frontier.update(problem.getStartNode())
    visited = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        visited.add(node)
        successors = problem.getSuccessors(node)
        for new_node in successors:
            if new_node not in visited:
                frontier.update(new_node)
    problem.storeResults(visited)


def graph_search(problem: SearchProblem, frontier):
    found_goal = False
    frontier.update(problem.getStartNode())
    visited = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoal(node):
            problem.storeResults(node)
            found_goal = True
            break
        if node not in visited:
            visited.add(node)
            successors = problem.getSuccessors(node)
            for new_node in successors:
                frontier.update(new_node)
    return found_goal
