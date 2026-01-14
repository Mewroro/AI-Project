from Algorithms.Problems.ProblemBase import ProblemBase

class HanoiProblem(ProblemBase):
    def __init__(self, n_disks, n_pegs=3):
        self.n = n_disks
        self.pegs = n_pegs
        self.type = "hanoi"

    def initial_state(self):
        return (tuple(range(self.n, 0, -1)),) + tuple(() for _ in range(self.pegs - 1))

    def is_goal(self, state):
        return state[-1] == tuple(range(self.n, 0, -1))

    def successors(self, state):
        successors = []

        for i in range(self.pegs):
            if not state[i]:
                continue

            disk = state[i][-1]

            for j in range(self.pegs):
                if i == j:
                    continue

                if not state[j] or state[j][-1] > disk:
                    new_state = list(list(peg) for peg in state)
                    new_state[i].pop()
                    new_state[j].append(disk)
                    successors.append(tuple(tuple(peg) for peg in new_state))

        return successors

    def heuristic(self, state):
        return sum(len(peg) for peg in state[:-1])
