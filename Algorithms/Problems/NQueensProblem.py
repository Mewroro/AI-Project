from Algorithms.Problems.ProblemBase import ProblemBase

class NQueensProblem(ProblemBase):
    def __init__(self, n):
        self.n = n
        self.type = "nqueens"

    def initial_state(self):
        return ()

    def is_goal(self, state):
        return len(state) == self.n

    def successors(self, state):
        row = len(state)
        successors = []

        for col in range(self.n):
            if self.is_safe(state, row, col):
                successors.append(state + (col,))
        return successors

    def is_safe(self, state, row, col):
        for r in range(row):
            if state[r] == col or abs(state[r] - col) == abs(r - row):
                return False
        return True

    def heuristic(self, state):
        conflicts = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts
