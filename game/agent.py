from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor
from .level import Level
from .util import GAME_TICKS_PER_SECOND, Loc, Node, Queue
from .search import graph_search, BlueprintSearchProblem


@dataclass
class Agent(ABC):
    name: str
    location: Loc
    parent: Level
    numGameTicks: int = 0
    priorLocation: Loc = None
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
        return GAME_TICKS_PER_SECOND / self.velocity


@dataclass
class Player(Agent):
    actions: list = field(default_factory=list)

    async def moveTo(self, pos: Loc):
        problem = BlueprintSearchProblem(self.parent.layout, Node(self.location), Node(pos))
        with ProcessPoolExecutor(max_workers=1) as executor:
            future = executor.submit(graph_search, problem, Queue())
        completed = future.result()
        self.actions = completed.actions if completed else []

    def update(self):
        self.numGameTicks += 1
        if self.numGameTicks > self.game_ticks_before_each_move:
            self.priorLocation = self.location
            self.location = self.actions.pop()
