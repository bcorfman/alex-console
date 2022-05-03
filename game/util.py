import heapq
from blessed import Terminal
from collections import deque
from dataclasses import dataclass


term = Terminal()

ROW_LENGTH = 80
PLAYER1_NAME = 'Brandon'
GAME_TICKS_PER_SECOND = 20
GAME_TICK = 1.0 / GAME_TICKS_PER_SECOND


@dataclass(eq=False)
class Loc:
    row: int
    col: int

    def __eq__(self, other):
        if isinstance(other, Loc):
            return self.row == other.row and self.col == other.col
        else:
            return self.row == other[0] and self.col == other[1]

    def __hash__(self):
        return hash((self.row, self.col))

    @classmethod
    def from_tuple(cls, t):
        loc = cls.__new__(cls)
        loc.row, loc.col = t
        return loc


class Node:
    def __init__(self, state, actions=None, cost=None):
        self.state = state
        self.actions = actions or []
        self.cost = cost or 0

    def __repr__(self):
        return f'Node({self.state}, {self.actions}, {self.cost})'

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.state == other.state
        elif isinstance(other, tuple):
            return self.state == other

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.cost < other.cost
        else:
            raise TypeError(f'Cannot compare Node to unknown type {type(other)}')

    def __hash__(self):
        return hash(self.state)


def loc_ordering(loc):
    return loc.row * ROW_LENGTH + loc.col


def manhattan_distance(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)


class Stack:
    def __init__(self):
        self._data = []

    def __repr__(self):
        return f'Stack({self._data})'

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def __delitem__(self, key):
        del self._data[key]

    def __contains__(self, item):
        return item in self._data

    def push(self, item, _priority=None):
        self._data.append(item)

    def pop(self):
        return self._data.pop()

    def isEmpty(self):
        return len(self._data) == 0

    def update(self, item, _priority=None):
        """ Add the item into the queue if not there; otherwise,
        update in place if cost is lower. """
        if item not in self._data:
            self._data.append(item)
        else:
            idx = self._data.index(item)
            if item.cost < self._data[idx].cost:
                self._data[idx] = item


class Queue:
    """ A container with a first-in-first-out (FIFO) queuing policy. """
    def __init__(self, lst=None):
        if lst is None:
            lst = []
        self._data = deque(lst)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f'Queue({self._data})'

    def __getitem__(self, item):
        return self._data[item]

    def __delitem__(self, key):
        del self._data[key]

    def __contains__(self, item):
        return item in self._data

    def push(self, item, _priority=None):
        self._data.appendleft(item)

    def pop(self):
        return self._data.pop()

    def isEmpty(self):
        return len(self._data) == 0

    def update(self, item, _priority=None):
        """ Add the item into the queue if not there; otherwise,
        update in place if cost is lower. """
        if item not in self._data:
            self._data.appendleft(item)
        else:
            idx = self._data.index(item)
            if item.cost < self._data[idx].cost:
                self._data[idx] = item


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def __init__(self, heap=None, _count=None):
        if heap is None:
            heap = []
        self._data = heap

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f'PriorityQueue({self._data})'

    def __contains__(self, item):
        for p, c, i in self._data:
            if i.state == item.state:
                return True
        return False

    def push(self, item, priority=None):
        if priority is None:
            priority = item.cost
        entry = (priority, len(self._data), item)
        heapq.heappush(self._data, entry)

    def pop(self):
        (_, _, item) = heapq.heappop(self._data)
        return item

    def isEmpty(self):
        return len(self._data) == 0

    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self._data):
            if i == item:
                if p <= priority:
                    break
                del self._data[index]
                self._data.append((priority, c, item))
                heapq.heapify(self._data)
                break
        else:
            self.push(item, priority)
