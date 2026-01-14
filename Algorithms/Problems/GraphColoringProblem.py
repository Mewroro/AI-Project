from Algorithms.Problems.ProblemBase import ProblemBase

class GraphColoringProblem(ProblemBase):
    def __init__(self, graph, colors):
        self.graph = graph
        self.colors = colors
        self.nodes = list(graph.keys())
        self.type = "coloring"

    def initial_state(self):
        return {}

    def is_goal(self, state):
        return len(state) == len(self.nodes)

    def successors(self, state):
        successors = []

        uncolored = [n for n in self.nodes if n not in state]
        if not uncolored:
            return []

        node = uncolored[0]

        for color in self.colors:
            if self.is_safe(state, node, color):
                new_state = dict(state)
                new_state[node] = color
                successors.append(new_state)

        return successors

    def is_safe(self, state, node, color):
        for neighbor in self.graph[node]:
            if neighbor in state and state[neighbor] == color:
                return False
        return True

    def heuristic(self, state):
        conflicts = 0
        for node, neighbors in self.graph.items():
            for n in neighbors:
                if node in state and n in state and state[node] == state[n]:
                    conflicts += 1
        return conflicts // 2
