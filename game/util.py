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


class Node:
    def __init__(self, state, actions=None, cost=None):
        self.state = state
        self.actions = actions or []
        self.cost = cost or 0

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.state == other.state
        elif isinstance(other, tuple):
            return self.state == other

    def __contains__(self, item):
        return self.state == item.state

    def __hash__(self):
        return hash(self.state)


@dataclass(frozen=True)
class Perimeter:
    top_left: Node
    bottom_right: Node

    def expand_border(self, amt=1):
        tl_row, tl_col = self.top_left.state
        br_row, br_col = self.bottom_right.state
        new_tl = tl_row - amt, tl_col - amt
        new_br = br_row + amt, br_col + amt
        return Perimeter(Node(new_tl), Node(new_br))

    def find_room_name(self, layout):
        tl_row, tl_col = self.top_left.state
        br_row, br_col = self.bottom_right.state
        chars = []
        for r in range(tl_row, br_row + 1):
            for c in range(tl_col, br_col + 1):
                if layout[r][c] != ROOM_CHAR:
                    chars.append(layout[r][c])
        return ''.join(chars).strip()


def node_ordering(node):
    loc_row, loc_col = node.state
    return loc_row * ROW_LENGTH + loc_col


# Data structures useful for implementing SearchAgents
class Stack:
    """ A container with a last-in-first-out (LIFO) queuing policy. """

    def __init__(self):
        self.list = []

    def __getitem__(self, item):
        return self.list[item]

    def __delitem__(self, key):
        del self.list[key]

    def update(self, item):
        """ Add the item into the queue if not there; otherwise,
        update in place if cost is lower. """
        if item not in self.list:
            self.list.append(item)
        else:
            idx = self.list.index(item)
            if item.cost < self.list[idx].cost:
                self.list[idx] = item

    def pop(self):
        """ Pop the most recently pushed item from the stack """
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0


class Queue:
    """ A container with a first-in-first-out (FIFO) queuing policy. """

    def __init__(self):
        self.deque = deque()

    def __getitem__(self, item):
        return self.deque[item]

    def __delitem__(self, key):
        del self.deque[key]

    def update(self, item):
        """ Add the item into the queue if not there; otherwise,
        update in place if cost is lower. """
        if item not in self.deque:
            self.deque.appendleft(item)
        else:
            idx = self.deque.index(item)
            if item.cost < self.deque[idx].cost:
                self.deque[idx] = item

    def pop(self):
        """ Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue. """
        return self.deque.pop()

    def isEmpty(self):
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
