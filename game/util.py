import os
import heapq
from blessed import Terminal
from collections import deque
from dataclasses import dataclass


term = Terminal()

ROW_LENGTH = 80
LEVEL1 = os.path.join(os.path.dirname(__file__), '..', 'levels', 'level1.txt')
PLAYER1_NAME = 'Brandon'
GAME_TICKS_PER_SECOND = 20
GAME_TICK = 1.0 / GAME_TICKS_PER_SECOND


@dataclass(eq=False)
class Loc:
    row: int
    col: int

    # def __iter__(self):
    #    yield self.row
    #    yield self.col

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

    def __hash__(self):
        return hash(self.state)


def node_ordering(node):
    return node.state.row * ROW_LENGTH + node.state.col


# Data structures useful for implementing SearchAgents
class Stack:
    """ A container with a last-in-first-out (LIFO) queuing policy. """
    def __init__(self, lst=None):
        if lst is None:
            lst = []
        self.list = lst

    def __repr__(self):
        return f'Stack({self.list})'

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
    def __init__(self, lst=None):
        if lst is None:
            lst = []
        self.deque = deque(lst)

    def __repr__(self):
        return f'Queue({self.deque})'

    def __getitem__(self, item):
        return self.deque[item]

    def __delitem__(self, key):
        del self.deque[key]

    def update(self, item):
        """ Add the item into the queue if not there; otherwise,
        update in place if cost is lower. """
        if item not in self.deque:
            self.deque.append(item)
        else:
            idx = self.deque.index(item)
            if item.cost < self.deque[idx].cost:
                self.deque[idx] = item

    def pop(self):
        """ Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue. """
        return self.deque.popleft()

    def isEmpty(self):
        return len(self.deque) == 0


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """

    def __init__(self, heap=None, count=None):
        if heap is None:
            heap = []
        self.heap = heap
        if count is None:
            count = 0
        self.count = count

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
