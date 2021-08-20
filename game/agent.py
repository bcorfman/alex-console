from dataclasses import dataclass
from abc import ABC, abstractmethod
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
