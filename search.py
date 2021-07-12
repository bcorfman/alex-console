from collections import namedtuple

SuccessorResults = namedtuple('SearchResults', ['nodes', 'outliers'])
SearchResults = namedtuple('SearchResults', ['visited', 'entrances', 'hallways'])


class BlueprintSearchProblem:
    def __init__(self, grid, start_loc, search_char):
        self.grid = grid
        self.start_loc = start_loc
        self.search_char = search_char
        self.hallways = set()
        self.rooms = []
        self.search_locations = set()

    def getStartState(self):
        return self.start_loc

    def getSuccessors(self, state, **kwargs) -> SuccessorResults:
        nodes = []
        fringe = []
        src_row, src_col = state
        valid_offsets = []
        for offset_row, offset_col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = src_row + offset_row, src_col + offset_col
            new_node = self.grid[new_row][new_col]
            if new_node == self.search_char:
                valid_offsets.append((offset_row, offset_col))
                nodes.append((new_row, new_col))
            elif new_node != ' ':
                fringe.append((new_row, new_col))
        cross_junction = len(valid_offsets) == 4
        t_or_corner_junction = (len(valid_offsets) > 1 and
                                (sum([row for row, _ in valid_offsets]) != 0 or
                                 sum([col for _, col in valid_offsets]) != 0))
        dead_end = len(valid_offsets) == 1 and self.getStartState() != (src_row, src_col)
        if cross_junction or t_or_corner_junction:
            self.hallways.add(frozenset(self.search_locations))
            self.hallways.add(frozenset([(src_row, src_col)]))
            self.search_locations.clear()
        elif dead_end:
            self.search_locations.add((src_row, src_col))
            self.hallways.add(frozenset(self.search_locations))
            self.search_locations.clear()
        elif state == self.getStartState() or not t_or_corner_junction:
            self.search_locations.add(state)
        else:
            raise ValueError('unrecognized junction type')
        return SuccessorResults(nodes=nodes, outliers=fringe)


def depth_first_search(problem: BlueprintSearchProblem, **kwargs) -> SearchResults:
    frontier = [problem.getStartState()]
    visited = set()
    room_entrances = set()
    while frontier:
        state = frontier.pop()
        visited.add(state)
        results = problem.getSuccessors(state, **kwargs)
        for node in results.nodes:
            if node not in visited:
                frontier.append(node)
        for outlier in results.outliers:
            if outlier not in room_entrances:
                room_entrances.add(outlier)
    return SearchResults(visited=list(visited), entrances=list(room_entrances),
                         hallways=list(problem.hallways))
