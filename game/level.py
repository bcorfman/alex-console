from dataclasses import dataclass
from itertools import chain

from .blueprint import Hallway, Perimeter, Room
from .characters import Player
from .chartypes import PLAYER_CHARS
from .search import HallwayConstructionProblem, exhaustive_search
from .util import PLAYER1_NAME, ROW_LENGTH, Loc, Node, loc_ordering


@dataclass(init=False)
class Level:
    hallways: list[Hallway]
    rooms: list[Room]
    elevators: list[Room]
    layout: list
    players: list[Player]

    def __init__(self, filename=None):
        self.hallways = []
        self.rooms = []
        self.elevators = []
        self.layout = []
        self.players = []
        if filename:
            self._load_layout(filename)
            self._add_border_to_layout()
            self._find_players()
            self._locate_elevators()
            self._find_rooms()

    def _load_layout(self, filename):
        with open(filename, encoding="utf-8") as f:
            self.layout = [line.rstrip() for line in f.readlines()]

    def _add_border_to_layout(self):
        lines = ["".ljust(ROW_LENGTH)]
        for line in self.layout:
            lines.append(line.rjust(len(line) + 1).ljust(ROW_LENGTH))
        lines.append(ROW_LENGTH * " ")
        self.layout = lines

    def _locate_elevators(self):
        self.elevators = []
        for row, r_item in enumerate(self.layout):
            col_length = len(r_item) - 3
            for col in range(col_length):
                if r_item[col:col + 4].upper() == "ELEV":
                    loc = Loc(row, col - 2)
                    problem = HallwayConstructionProblem(self.layout, Node(loc), Room.mapChar)
                    exhaustive_search(problem)
                    p = Perimeter(
                        min(problem.visited, key=loc_ordering),
                        max(problem.visited, key=loc_ordering),
                    )
                    exits = self._identify_room_exits(p)
                    self.elevators.append(Room("ELEVATOR", p, exits))

    def _search_for_exit_in_row(self, row, start, end):
        exit_ = None
        for i in range(start, end):
            if self.layout[row][i] == Hallway.mapChar:
                exit_ = Loc(row, i)
                break
        return exit_

    def _search_for_exit_in_col(self, col, start, end):
        exit_ = None
        for i in range(start, end):
            if self.layout[i][col] == Hallway.mapChar:
                exit_ = Loc(i, col)
                break
        return exit_

    def _identify_room_exits(self, room_perimeter):
        new_perimeter = room_perimeter.expand_border()
        tl_row, tl_col = new_perimeter.top_left.row, new_perimeter.top_left.col
        br_row, br_col = new_perimeter.bottom_right.row, new_perimeter.bottom_right.col
        exits = [
            self._search_for_exit_in_row(tl_row, tl_col, br_col + 1),
            self._search_for_exit_in_row(br_row, tl_col, br_col + 1),
            self._search_for_exit_in_col(tl_col, tl_row, br_row + 1),
            self._search_for_exit_in_col(br_col, tl_row, br_row + 1),
        ]
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
            problem = HallwayConstructionProblem(self.layout, Node(elevator.exits[0]),
                                                 Hallway.mapChar)
            exhaustive_search(problem)
            room_entrances = problem.room_entrances
            self.hallways.extend(problem.hallways)
            # Collect information on each new room. Don't consider rooms that have already been
            # found.
            for entrance in room_entrances:
                problem = HallwayConstructionProblem(self.layout, Node(entrance), Room.mapChar)
                exhaustive_search(problem)
                p = Perimeter(
                    min(problem.visited, key=loc_ordering),
                    max(problem.visited, key=loc_ordering),
                )
                if p not in perimeters_found:
                    name = p.find_room_name(self.layout)
                    exits = self._identify_room_exits(p)
                    perimeters_found.add(p)
                    self.rooms.append(Room(name, p, exits))

    def _find_players(self):
        for r, row in enumerate(self.layout):
            for c, _col in enumerate(row):
                if self.layout[r][c] in PLAYER_CHARS:
                    self.players.append(
                        Player(
                            name=PLAYER1_NAME,
                            velocity=5,
                            location=Loc(r, c),
                            parent=self,
                        ))
                    # once player has been recorded, replace player char on map with either a
                    # hallway or room char so hallways and rooms are constructed correctly later
                    # in __init__.
                    if (self.layout[r][c - 1] == Hallway.mapChar
                            and self.layout[r][c + 1] == Hallway.mapChar):
                        self.layout[r] = (self.layout[r][:c] + Hallway.mapChar +
                                          self.layout[r][c + 1:])
                    elif (self.layout[r][c - 1] == Room.mapChar
                          and self.layout[r][c + 1] == Room.mapChar):
                        self.layout[r] = (self.layout[r][:c] + Room.mapChar +
                                          self.layout[r][c + 1:])

    def get_first_player(self):
        return self.players[0]

    def check_for_player(self, loc: Loc):
        found_player = None
        for player in self.players:
            if player.location == loc:
                found_player = player
        return found_player

    def is_valid_map_location(self, loc: Loc):
        return self.layout[loc.row][loc.col] != " "

    def translate_char(self, row, col):
        for elem in chain(self.elevators, self.rooms, self.hallways):
            if self.layout[row][col] == elem.mapChar:
                output = elem.color + elem.displayChar
                break
        else:
            output = self.layout[row][col]
        return output

    async def update(self):
        for player in self.players:
            player.update()
        return True
