import re

class CSPAnswerChecker:
    PARTIAL_RESPONSE_THRESHOLD = 0.5

    def __init__(self):
        pass

    def get_csp_feedback(self, answer, user_answer, explanation):
        feedback = {}
        points = 0

        user_assignment = self.parse_assignment(user_answer)

        if self.user_says_no_solution(user_answer):
            points = 100 if answer is None else 0
        else:
            if not user_assignment:
                points = 0
            elif answer is None:
                points = 0
            else:
                points = self.check_assignment(answer, user_assignment)

        if points == 100:
            feedback["message"] = "Raspuns corect!"
        elif points >= 50:
            feedback["message"] = "Raspuns partial corect! " + explanation
        else:
            feedback["message"] = "Raspuns gresit. " + explanation

        feedback["points"] = points
        feedback["correct_answer"] = self.format_solution(answer)

        return feedback

    def user_says_no_solution(self, user_answer):
        user_answer = user_answer.lower().strip()
        return user_answer in ["nu exista solutie", "fara solutie", "none", "nu"]

    def parse_assignment(self, user_answer):
        pattern = r"([A-Za-z]+)\s*=\s*([0-9]+)"
        matches = re.findall(pattern, user_answer)

        assignment = {}
        for var, val in matches:
            assignment[var.upper()] = int(val)

        return assignment

    def check_assignment(self, solution, user_assignment):
        total_vars = len(solution)
        correct_count = 0

        for var, val in user_assignment.items():
            if var not in solution or solution[var] != val:
                return 0
            correct_count += 1

        ratio = correct_count / total_vars
        if ratio == 1:
            return 100
        elif ratio >= self.PARTIAL_RESPONSE_THRESHOLD:
            return 50
        else:
            return 0

    def format_solution(self, solution):
        if solution is None:
            return "Nu exista solutie"

        parts = [f"{var}={solution[var]}" for var in sorted(solution.keys())]
        return "O asignare valida ar fi: " + " ".join(parts)
