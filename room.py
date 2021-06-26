from dataclasses import dataclass
from chartypes import HALLWAY_CHAR


@dataclass
class Perimeter:
    top_left_row: int
    top_left_col: int
    bottom_right_row: int
    bottom_right_col: int


class Room:
    def __init__(self, name, top_left, bottom_right):
        self.name = name
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.exits = []

    def search_for_exit_in_row(self, layout, row, start, end):
        for i in range(start, end):
            if layout[row][i] == HALLWAY_CHAR:
                self.exits.append((row, i))

    def search_for_exit_in_col(self, layout, col, start, end):
        for i in range(start, end):
            if layout[i][col] == HALLWAY_CHAR:
                self.exits.append((i, col))

    def identify_exits(self, layout):
        tl_row, tl_col = self.top_left
        br_row, br_col = self.bottom_right
        p = Perimeter(top_left_row=tl_row - 1, top_left_col=tl_col - 1, bottom_right_row=br_row + 1,
                      bottom_right_col=br_col + 1)
        self.search_for_exit_in_row(layout, p.top_left_row, p.top_left_col, p.bottom_right_col + 1)
        self.search_for_exit_in_row(layout, p.bottom_right_row, p.top_left_col, p.bottom_right_col + 1)
        self.search_for_exit_in_col(layout, p.top_left_row, p.top_left_col, p.bottom_right_col + 1)
        self.search_for_exit_in_col(layout, p.bottom_right_row, p.top_left_col, p.bottom_right_col + 1)
