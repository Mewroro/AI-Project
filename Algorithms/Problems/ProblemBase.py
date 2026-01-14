from abc import ABC, abstractmethod

class ProblemBase(ABC):
    @abstractmethod
    def initial_state(self):
        pass

    @abstractmethod
    def is_goal(self, state):
        pass

    @abstractmethod
    def successors(self, state):
        pass

    def cost(self, state, next_state):
        return 1

    def heuristic(self, state):
        return 0
