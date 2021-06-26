from room import Room
from chartypes import ROOM_CHAR


def load_layout(filename):
    with open(filename) as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        lines[i] = line.rstrip().ljust(70, ' ')
    lines.append(70 * ' ')  # extra line as buffer around outer edge. Avoids boundary checks during expand method.
    return lines


def expand(layout, loc, char):
    nodes = []
    src_row, src_col = loc
    for row, col in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = src_row + row, src_col + col
        if layout[new_row][new_col] == char:
            nodes.append((new_row, new_col))
    return nodes


def depth_first_search(layout, row, col, char):
    start_node = (row, col)
    frontier = [start_node]
    visited = set()
    visited.add(start_node)  # because if I just try to pass the tuple into the set __init__, it treats it as two ints
    while frontier:
        loc = frontier.pop()
        for item in expand(layout, loc, char):
            if item not in visited:
                visited.add(item)
                frontier.append(item)
    return list(visited)


def location_ordering(loc):
    row, col = loc
    return row * 100 + col


def find_elevators(layout):
    elevators = []
    for row, r_item in enumerate(layout):
        col_length = len(r_item) - 3
        for col in range(col_length):
            if r_item[col:col + 4].upper() == 'ELEV':
                locations = depth_first_search(layout, row, col - 2, ROOM_CHAR)
                elevators.append(Room('ELEVATOR',
                                      min(locations, key=location_ordering),
                                      max(locations, key=location_ordering)))
    return elevators
