from .util import term


class Hallway:
    mapChar = '~'
    color = term.white
    displayChar = term.reverse(' ')

    def __init__(self, locations):
        self.locations = frozenset(locations)

    def __eq__(self, other):
        if isinstance(other, frozenset):
            return self.locations == other
        else:
            return self.locations == other.locations

    def __contains__(self, item):
        return item in self.locations

    def __hash__(self):
        return hash(self.locations)

    @classmethod
    def from_list(cls, lst):
        hallway = cls.__new__(cls)
        hallway.locations = frozenset(lst)
        return hallway
