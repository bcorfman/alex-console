import sys
import os
from dataclasses import dataclass
from .chartypes import ROOM_CHAR


def get_cwd():
    try:
        wd = sys._MEIPASS
    except AttributeError:
        wd = os.getcwd()
    return wd


ROW_LENGTH = 80
LEVEL1 = os.path.join(get_cwd(), 'levels', 'level1.txt')


@dataclass(frozen=True)
class Perimeter:
    top_left: tuple[int, int]
    bottom_right: tuple[int, int]

    def expand_border(self, amt=1):
        tl_row, tl_col = self.top_left
        br_row, br_col = self.bottom_right
        return Perimeter((tl_row - amt, tl_col - amt), (br_row + amt, br_col + amt))

    def find_room_name(self, layout):
        tl_row, tl_col = self.top_left
        br_row, br_col = self.bottom_right
        chars = []
        for r in range(tl_row, br_row + 1):
            for c in range(tl_col, br_col + 1):
                if layout[r][c] != ROOM_CHAR:
                    chars.append(layout[r][c])
        return ''.join(chars).strip()


def location_ordering(loc):
    loc_row, loc_col = loc
    return loc_row * ROW_LENGTH + loc_col
