from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Loc:
    row: int
    col: int


@dataclass
class Agent(ABC):
    name: str
    velocity: int  # cells per second
    location: Loc
    parent: object

    @abstractmethod
    def moveTo(self, pos: Loc):
        """ Plots the shortest path between the current location and the provided location using
        search. Updates the movement along the path during each game loop call to self.update().
        Returns True if a path is found; False otherwise"""

    @abstractmethod
    def update(self, t):
        """ Should be called during each iteration of the game loop to update the position
        of the agent. t is the delta time in seconds that has passed.
        Return None."""
