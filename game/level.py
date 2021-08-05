from .room import Room
from .util import node_ordering, ROW_LENGTH, Perimeter, Node, PLAYER1_NAME
from .search import exhaustive_search, HallwayConstructionProblem
from .chartypes import ROOM_CHARS, HALLWAY_CHARS, PLAYER_CHARS
from .agent import Loc
from .player import Player


class Level:
    def __init__(self, filename=None):
        self.hallways = []
        self.rooms = []
        self.elevators = []
        self.layout = []
        self.players = []
        if filename:
            self._load_layout(filename)
            self._add_border_to_layout()
            self._find_elevators()
            self._find_rooms()
            self._find_players()

    def _load_layout(self, filename):
        with open(filename) as f:
            self.layout = [line.rstrip() for line in f.readlines()]

    def _add_border_to_layout(self):
        lines = [''.ljust(ROW_LENGTH)]
        for line in self.layout:
            lines.append(line.rjust(len(line) + 1).ljust(ROW_LENGTH))
        lines.append(ROW_LENGTH * ' ')
        self.layout = lines

    def _find_elevators(self):
        self.elevators = []
        for row, r_item in enumerate(self.layout):
            col_length = len(r_item) - 3
            for col in range(col_length):
                if r_item[col:col + 4].upper() == 'ELEV':
                    loc = (row, col - 2)
                    problem = HallwayConstructionProblem(self.layout, Node(loc), ROOM_CHARS)
                    exhaustive_search(problem)
                    p = Perimeter(min(problem.visited, key=node_ordering),
                                  max(problem.visited, key=node_ordering))
                    exits = self._identify_room_exits(p)
                    self.elevators.append(Room('ELEVATOR', p, exits))

    def _search_for_exit_in_row(self, row, start, end):
        exit_ = None
        for i in range(start, end):
            if self.layout[row][i] in HALLWAY_CHARS:
                exit_ = row, i
                break
        return exit_

    def _search_for_exit_in_col(self, col, start, end):
        exit_ = None
        for i in range(start, end):
            if self.layout[i][col] in HALLWAY_CHARS:
                exit_ = i, col
                break
        return exit_

    def _identify_room_exits(self, room_perimeter):
        new_perimeter = room_perimeter.expand_border()
        tl_row, tl_col = new_perimeter.top_left.state
        br_row, br_col = new_perimeter.bottom_right.state
        exits = [self._search_for_exit_in_row(tl_row, tl_col, br_col + 1),
                 self._search_for_exit_in_row(br_row, tl_col, br_col + 1),
                 self._search_for_exit_in_col(tl_col, tl_row, br_row + 1),
                 self._search_for_exit_in_col(br_col, tl_row, br_row + 1)]
        return [e for e in exits if e is not None]

    def _find_rooms(self):
        self.rooms = []
        self.hallways = []
        # add elevators to the list of room perimeters, so they aren't included in search.
        perimeters_found = set()
        for elevator in self.elevators:
            perimeters_found.add(elevator.perimeter)
        # pick first exit of each elevator as a starting point for search
        for elevator in self.elevators:
            problem = HallwayConstructionProblem(self.layout, Node(elevator.exits[0]), HALLWAY_CHARS)
            exhaustive_search(problem)
            locations, room_entrances = problem.visited, problem.room_entrances
            self.hallways.extend(problem.hallways)
            # Collect information on each new room. Don't consider rooms that have already been found.
            for entrance in room_entrances:
                problem = HallwayConstructionProblem(self.layout, Node(entrance), ROOM_CHARS)
                exhaustive_search(problem)
                p = Perimeter(min(problem.visited, key=node_ordering),
                              max(problem.visited, key=node_ordering))
                if p not in perimeters_found:
                    name = p.find_room_name(self.layout)
                    exits = self._identify_room_exits(p)
                    perimeters_found.add(p)
                    self.rooms.append(Room(name, p, exits))

    def _find_players(self):
        for r, row in enumerate(self.layout):
            for c, col in enumerate(row):
                if self.layout[r][c] in PLAYER_CHARS:
                    self.players.append(Player(PLAYER1_NAME, 2, Loc(r, c), self))
