from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor
from .util import Node, Queue, term
from .search import BlueprintSearchProblem, graph_search
from .util import Loc, GAME_TICKS_PER_SECOND


@dataclass
class Agent(ABC):
    name: str
    location: Loc
    parent: ...
    numGameTicks: int = 0
    velocity: int = 1  # cells per second

    @abstractmethod
    def moveTo(self, pos: Loc):
        """ Plots the shortest path between the current location and the provided location using
        search. Updates the movement along the path during each game loop call to self.update().
        Returns True if a path is found; False otherwise"""

    @abstractmethod
    def update(self):
        """ Should be called during each iteration of the game loop to update the position
        of the agent.
        Return None."""

    @property
    def game_ticks_before_each_move(self):
        return GAME_TICKS_PER_SECOND // self.velocity


@dataclass
class Player(Agent):
    actions: Queue = field(default_factory=Queue)
    mapChar: str = '!'
    priorMapChar: str = ''
    priorLocation: Loc = None
    displayChar: str = term.reverse('\u25CF')

    async def moveTo(self, pos: Loc):
        # noinspection PyUnresolvedReferences
        problem = BlueprintSearchProblem(self.parent.layout, Node(self.location), Node(pos))
        with ProcessPoolExecutor(max_workers=1) as executor:
            future = executor.submit(graph_search, problem, Queue())
        completed = future.result()
        self.actions = Queue(completed.actions) if completed else Queue()

    def update(self):
        self.numGameTicks += 1
        if self.numGameTicks > self.game_ticks_before_each_move:
            if not self.actions.isEmpty():
                self.priorLocation = self.location
                row, col = self.priorLocation.row, self.priorLocation.col
                self.priorMapChar = self.parent.layout[row][col]
                self.location = self.actions.pop()
            self.numGameTicks = 0
