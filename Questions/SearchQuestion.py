import random

from Algorithms.Problems.GraphColoringProblem import GraphColoringProblem
from Algorithms.Problems.HanoiProblem import HanoiProblem
from Algorithms.Problems.NQueensProblem import NQueensProblem
from Algorithms.Problems.KnightsTourProblem import KnightsTourProblem
from Algorithms.SearchStrategies import SearchStrategies
from Questions.QuestionBase import QuestionBase


class SearchQuestion(QuestionBase):
    def __init__(self):
        super().__init__("search")
        self.strategy_runner = SearchStrategies()

    def generate_nqueens_problem(self, N):
        return NQueensProblem(N)

    def generate_hanoi_problem(self, N, P):
        return HanoiProblem(N, P)

    def generate_graph_coloring_problem(self, V, E, K):
        graph = self.generate_random_graph(V, E)
        colors = [f"C{i}" for i in range(1, K + 1)]
        problem = GraphColoringProblem(graph, colors)
        graph_str = self.graph_to_string(graph)
        return problem, graph_str

    def generate_random_graph(self, V, E):
        edges = set()
        while len(edges) < E:
            u = random.randint(0, V - 1)
            v = random.randint(0, V - 1)
            if u != v:
                edges.add((min(u, v), max(u, v)))
        graph = {i: [] for i in range(V)}
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        return graph

    def graph_to_string(self, graph):
        lines = []
        for node, neighbors in graph.items():
            neighbors_str = ", ".join(str(n) for n in neighbors)
            lines.append(f"{node}: [{neighbors_str}]")
        return "\n".join(lines)

    def generate_knights_tour_problem(self, N):
        return KnightsTourProblem(N)

    def generate(self):
        template = self.get_random_template()
        question_id = template["id"]
        question_text = template["template"]
        explanation = template.get("explanation", "")

        values = {}
        for var in template["vars"]:
            value = random.randint(var["min-val"], var["max-val"])
            question_text = question_text.replace("{" + var["name"] + "}", str(value))
            values[var["name"]] = value

        problem = None
        if question_id == 1:
            problem = self.generate_nqueens_problem(values["N"])
        elif question_id == 2:
            problem = self.generate_hanoi_problem(values["N"], values["P"])
        elif question_id == 3:
            K = values.get("K", min(4, values["V"]))
            problem, graph_str = self.generate_graph_coloring_problem(values["V"], values["E"], K)
            question_text = question_text.replace("{GRAPH}", "\n" + graph_str)
            question_text = question_text.replace("{K}", str(K))
        elif question_id == 4:
            problem = self.generate_knights_tour_problem(values["N"])

        self.strategy_runner.run_all(problem)
        answer = self.strategy_runner.best_strategy() #de tip ("nume strategie", timp)

        return question_text, question_id, answer, explanation
