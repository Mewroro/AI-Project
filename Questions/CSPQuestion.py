import random
from Algorithms.CSP import CSP
from Questions.QuestionBase import QuestionBase

class CSPQuestion(QuestionBase):
    def __init__(self):
        super().__init__("csp")

    def generate_variable_names(self, count):
        return [chr(ord('A') + i) for i in range(count)]

    def get_random_constraint(self):
        constraints = [
            ("≠", self.not_equal, self.not_equal),
            ("<", self.less_than, self.greater_than),
            (">", self.greater_than, self.less_than),
            ("≤", self.less_equal, self.greater_equal),
            ("≥", self.greater_equal, self.less_equal),
        ]
        return random.choice(constraints)

    def get_answer(self, question_id, csp):
        if question_id == 1:
            return csp.backtracking(use_fc=True)

        if question_id == 2:
            return csp.backtracking(use_mrv=True)

        if question_id == 3:
            return csp.backtracking(use_ac3=True)

        return None
    def generate(self):
        question = self.get_random_template()
        question_id = question["id"]
        template = question["template"]
        variable = question["vars"][0]
        explanation = question["explanation"]

        variable_count = random.randint(variable["min-vars"], variable["max-vars"])
        min_domain_size = variable["min-domain"]
        max_domain_size = variable["max-domain"]

        variables = self.generate_variable_names(variable_count)

        domains = {}
        for v in variables:
            domain_size = random.randint(min_domain_size, max_domain_size)
            domains[v] = list(range(min_domain_size, domain_size + 1))

        constraints = {}
        constraint_labels = {}

        for i in range(len(variables) - 1):
            a, b = variables[i], variables[i + 1]

            symbol, ab_function, ba_function = self.get_random_constraint()

            constraints[(a, b)] = ab_function
            constraints[(b, a)] = ba_function

            constraint_labels[(a, b)] = symbol
            constraint_labels[(b, a)] = self.inverse_symbol(symbol)

        assigned_var = variables[0]
        assigned_value = random.choice(domains[assigned_var])
        assignments = {assigned_var: assigned_value}

        text = self.csp_to_string(variables, domains, constraints, assignments, constraint_labels)
        question_text = template.replace("{X}", "\n" + text)

        csp = CSP(variables, domains, constraints, assignments)
        answer = self.get_answer(question_id, csp)

        return question_text, answer, explanation

    def csp_to_string(self, variables, domains, constraints, assignments, constraint_labels):
        lines = []
        lines.append("Variabile: " + ", ".join(variables))
        lines.append("Domenii:")
        for v in variables:
            lines.append(f"{v} ∈ {domains[v]}")

        lines.append("\nConstrangeri:")
        seen = set()
        for (a, b) in constraints:
            if (a, b) not in seen:
                symbol = constraint_labels[(a, b)]
                lines.append(f"{a} {symbol} {b}")
                seen.add((a, b))
                seen.add((b, a))

        lines.append("\nAsignare partiala:")
        for v, val in assignments.items():
            lines.append(f"{v} = {val}")

        return "\n".join(lines)

    def not_equal(self, x, y):
        return x != y

    def less_than(self, x, y):
        return x < y

    def greater_than(self, x, y):
        return x > y

    def less_equal(self, x, y):
        return x <= y

    def greater_equal(self, x, y):
        return x >= y

    def inverse_symbol(self, symbol):
        return {
            "<": ">",
            ">": "<",
            "≤": "≥",
            "≥": "≤",
            "≠": "≠"
        }[symbol]
