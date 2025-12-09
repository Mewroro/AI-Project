import random

from Algorithms.Nash import Nash
from Questions.QuestionBase import QuestionBase

class NashQuestion(QuestionBase):
    def __init__(self):
        super().__init__("nash")

    def get_answer(self, id, nash):
        nash.find_pure_nash()
        if id == 1 or id == 3:
            return nash.equilibrium_count
        if id == 2:
            return nash.equilibria
        if id == 4:
            return nash.get_player1_dominant_strategies()
        if id == 5:
            return nash.get_player2_dominant_strategies()

        return None
    def generate_strategy_names(self, count, sufix):
        return [f"{chr(ord('A') + i)}{sufix}" for i in range(count)]

    def generate(self):
        question = self.get_random_template()
        question_id = question["id"]
        template = question["template"]
        variable = question["vars"][0]
        explanation = question["explanation"]

        row_count = random.randint(variable["min-strategies-count"], variable["max-strategies-count"])
        column_count = random.randint(variable["min-strategies-count"], variable["max-strategies-count"])

        name = variable["name"]
        min_payoff = variable["min-payoff"]
        max_payoff = variable["max-payoff"]

        is_mixt = variable["is_mixt"]

        matrix = [[(0, 0) for _ in range(column_count)] for _ in range(row_count)]

        x = random.randint(min_payoff, max_payoff)
        for row in range(row_count):
            for column in range(column_count):
                if is_mixt:
                    matrix[row][column] = (-x, x) if (row + column) % 2 == 0 else (x, -x)
                    continue

                player1_payoff = random.randint(min_payoff, max_payoff)
                player2_payoff = random.randint(min_payoff, max_payoff)
                matrix[row][column] = (player1_payoff, player2_payoff)

        player1_strategies = self.generate_strategy_names(row_count, "1")
        player2_strategies = self.generate_strategy_names(column_count, "2")

        matrix_string = self.matrix_to_string(matrix, player1_strategies, player2_strategies)
        question_text = template.replace("{" + name + "}", "\n" + str(matrix_string))

        nash = Nash(matrix, player1_strategies, player2_strategies)
        answer = self.get_answer(question_id, nash)

        return question_text, answer, matrix, player1_strategies, player2_strategies, explanation

    def matrix_to_string(self, matrix, player1_strategies, player2_strategies):
        lines = []

        header = "      " + " | ".join(f"{s:>5}" for s in player2_strategies)
        lines.append(header)
        lines.append("-" * len(header))

        for i, row in enumerate(matrix):
            row_str = " | ".join(f"({a:>2},{b:<2})" for a, b in row)
            lines.append(f"{player1_strategies[i]:>3} | {row_str}")

        return "\n".join(lines)



