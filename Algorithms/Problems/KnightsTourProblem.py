from Algorithms.Problems.ProblemBase import ProblemBase

class KnightsTourProblem(ProblemBase):
    def __init__(self, n):
        self.n = n
        self.moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        self.type = "knight"

    def initial_state(self):
        return ((0, 0),)

    def is_goal(self, state):
        return len(state) == self.n * self.n

    def successors(self, state):
        x, y = state[-1]
        successors = []

        for dx, dy in self.moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.n and 0 <= ny < self.n:
                if (nx, ny) not in state:
                    successors.append(state + ((nx, ny),))
        return successors

    def heuristic(self, state):
        return self.n * self.n - len(state)
