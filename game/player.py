from .util import Node, Queue
from .agent import Agent, Loc
from .search import graph_search, BlueprintSearchProblem


class Player(Agent):
    def moveTo(self, pos: Loc):
        problem = BlueprintSearchProblem(self.parent.layout, Node(self.location), Node(pos))
        actions = []
        if graph_search(problem, Queue()):
            actions.extend(problem.actions)
        return actions

    def update(self, t):
        pass
