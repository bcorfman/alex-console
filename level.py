from dataclasses import dataclass, field
from room import Room
from util import location_ordering, ROW_LENGTH, Perimeter
from search import depth_first_search
from chartypes import ROOM_CHAR, HALLWAY_CHAR


@dataclass
class Level:
    hallways: list[tuple[int, int]] = field(default_factory=list)
    rooms: list[Room] = field(default_factory=list)
    elevators: list[Room] = field(default_factory=list)
    _layout: list = field(default_factory=list)

    def __init__(self, filename=None):
        if filename:
            self._load(filename)
            self._find_elevators()
            self._find_rooms()

    def _load(self, filename):
        # extra line as buffer around top edge. Avoids boundary checks during self.expand
        self._layout = [''.ljust(ROW_LENGTH, ' ')]
        with open(filename) as f:
            self._layout.extend(f.readlines())
        for i, line in enumerate(self._layout):
            self._layout[i] = line.rstrip().ljust(ROW_LENGTH, ' ')
        # extra line as buffer around bottom edge. Avoids boundary checks during expand method.
        self._layout.append(ROW_LENGTH * ' ')

    def _find_elevators(self):
        self.elevators = []
        for row, r_item in enumerate(self._layout):
            col_length = len(r_item) - 3
            for col in range(col_length):
                if r_item[col:col + 4].upper() == 'ELEV':
                    locations, _ = depth_first_search(self._layout, row, col - 2, ROOM_CHAR)
                    p = Perimeter(min(locations, key=location_ordering),
                                  max(locations, key=location_ordering))
                    exits = self._identify_room_exits(p)
                    self.elevators.append(Room('ELEVATOR', p, exits))

    def _search_for_exit_in_row(self, row, start, end):
        exit_ = None
        for i in range(start, end):
            if self._layout[row][i] == HALLWAY_CHAR:
                exit_ = row, i
                break
        return exit_

    def _search_for_exit_in_col(self, col, start, end):
        exit_ = None
        for i in range(start, end):
            if self._layout[i][col] == HALLWAY_CHAR:
                exit_ = i, col
                break
        return exit_

    def _identify_room_exits(self, room_perimeter):
        new_perimeter = room_perimeter.expand_border()
        tl_row, tl_col = new_perimeter.top_left
        br_row, br_col = new_perimeter.bottom_right
        exits = [self._search_for_exit_in_row(tl_row, tl_col, br_col + 1),
                 self._search_for_exit_in_row(br_row, tl_col, br_col + 1),
                 self._search_for_exit_in_col(tl_col, tl_row, br_row + 1),
                 self._search_for_exit_in_col(br_col, tl_row, br_row + 1)]
        return [e for e in exits if e is not None]

    def _find_rooms(self):
        self.rooms = []
        # pick first exit of first elevator as a starting point for search
        exit_row, exit_col = self.elevators[0].exits[0]
        self.hallways, room_entrances = depth_first_search(self._layout, exit_row, exit_col, HALLWAY_CHAR, True)
        perimeters_found = set()
        for elevator in self.elevators:
            perimeters_found.add(elevator.perimeter)
        # Collect information on each new room. Don't consider rooms that have already been found.
        for entrance_row, entrance_col in room_entrances:
            room_locations, _ = depth_first_search(self._layout, entrance_row, entrance_col, ROOM_CHAR)
            p = Perimeter(min(room_locations, key=location_ordering),
                          max(room_locations, key=location_ordering))
            if p not in perimeters_found:
                name = p.find_room_name(self._layout)
                exits = self._identify_room_exits(p)
                perimeters_found.add(p)
                self.rooms.append(Room(name, p, exits))
