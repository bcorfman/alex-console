import sys
import os
import heapq
from collections import deque
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


# Data structures useful for implementing SearchAgents
class Stack:
    """ A container with a last-in-first-out (LIFO) queuing policy. """

    def __init__(self):
        self.list = []

    def __iter__(self):
        return self.list.__iter__()

    def push(self, item):
        """ Push 'item' onto the stack """
        self.list.append(item)

    def pop(self):
        """ Pop the most recently pushed item from the stack """
        return self.list.pop()

    def isEmpty(self):
        """ Returns true if the stack is empty """
        return len(self.list) == 0


class Queue:
    """ A container with a first-in-first-out (FIFO) queuing policy. """

    def __init__(self):
        self.deque = deque()

    def __iter__(self):
        return self.deque.__iter__()

    def push(self, item):
        """ Enqueue the 'item' into the queue. """
        self.deque.appendleft(item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.deque.pop()

    def isEmpty(self):
        """ Returns true if the queue is empty. """
        return len(self.deque) == 0


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
