from .agent import Agent, Loc


class Player(Agent):
    def moveTo(self, pos: Loc):
        return False

    def update(self):
        pass
