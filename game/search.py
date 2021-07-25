from abc import ABC, abstractmethod
from .util import Stack


class Node:
    def __init__(self, state, actions, cost):
        self.state = state
        self.actions = actions
        self.cost = cost

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)


class SearchProblem(ABC):
    @abstractmethod
    def getStartState(self):
        """ Returns the start state for the search. """

    @abstractmethod
    def isGoal(self, state, frontier):
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
    def __init__(self, grid, start_loc, goal_loc):
        self._grid = grid
        self._start_loc = start_loc
        self._goal_loc = goal_loc
        self.actions = []

    def getStartState(self):
        return self._start_loc, (), 0

    def isGoal(self, node, _):
        return node == self._goal_loc

    def storeResults(self, actions):
        self.actions = list(actions)

    def getSuccessors(self, state):
        nodes = []
        src_row, src_col = state
        for offset_row, offset_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = src_row + offset_row, src_col + offset_col
            new_node = self._grid[new_row][new_col]
            if new_node != ' ':
                nodes.append((new_row, new_col))
        return nodes


class HallwayConstructionProblem(SearchProblem):
    def __init__(self, grid, start_loc, search_char):
        self._grid = grid
        self.fringe = []
        self._start_loc = start_loc
        self._search_char = search_char
        self.hallways = set()
        self.rooms = []
        self._search_locations = set()
        self.room_entrances = set()
        self._goal = None
        self.visited = None

    def getStartState(self):
        return self._start_loc

    def getSuccessors(self, node):
        nodes = []
        src_row, src_col = node
        valid_offsets = []
        for offset_row, offset_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = src_row + offset_row, src_col + offset_col
            new_node = self._grid[new_row][new_col]
            if new_node == self._search_char:
                valid_offsets.append((offset_row, offset_col))
                nodes.append((new_row, new_col))
            elif new_node != ' ':
                self.fringe.append((new_row, new_col))
        cross_junction = len(valid_offsets) == 4
        t_or_corner_junction = (len(valid_offsets) > 1 and
                                (sum([row for row, _ in valid_offsets]) != 0 or
                                 sum([col for _, col in valid_offsets]) != 0))
        dead_end = len(valid_offsets) == 1 and self.getStartState() != (src_row, src_col)
        if cross_junction or t_or_corner_junction:
            self.hallways.add(frozenset(self._search_locations))
            self.hallways.add(frozenset([(src_row, src_col)]))
            self._search_locations.clear()
        elif dead_end:
            self._search_locations.add((src_row, src_col))
            self.hallways.add(frozenset(self._search_locations))
            self._search_locations.clear()
        elif node == self.getStartState() or not t_or_corner_junction:
            self._search_locations.add(node)
        else:
            raise ValueError('unrecognized junction type')
        return nodes

    def isGoal(self, node, _):
        return NotImplementedError

    def storeResults(self, visited_nodes):
        self.visited = visited_nodes
        for outlier in self.fringe:
            if outlier not in self.room_entrances:
                self.room_entrances.add(outlier)


def exhaustive_search(problem):
    """ Search until all nodes have been expanded, then return results. """
    frontier = Stack()
    frontier.push(problem.getStartState())
    visited = set()
    while not frontier.isEmpty():
        node = frontier.pop()
        visited.add(node)
        successors = problem.getSuccessors(node)
        for s in successors:
            if s not in visited and s not in frontier:
                frontier.push(s)
    problem.storeResults(visited)


def graph_search(problem, frontier):
    found_goal = False
    frontier.push(problem.getStartState())
    visited = set()
    while not frontier.isEmpty():
        state = frontier.pop()
        node, actions, cost = state
        if problem.isGoal(node, frontier):
            problem.storeResults(actions)
            found_goal = True
            break
        if state not in visited:
            visited.add(state)
            successors = problem.getSuccessors(node)
            for new_node in successors:
                new_actions = actions + (new_node,)
                new_cost = problem.getCostOfActions(new_actions)
                if new_node not in visited:
                    frontier.push((new_node, new_actions, new_cost))
                elif new_node in frontier:
                    incumbent = frontier[new_node]  # WHAT??
                    if new_cost < cost:
                        del frontier[incumbent]
                        frontier.push((new_node, new_actions, new_cost))
    return found_goal
