class SearchAnswerChecker:
    def __init__(self):
        self.valid_strategies = {
            1: ["backtracking", "hillclimbing", "simulated annealing"],
            2: ["bfs", "a*"],
            3: ["backtracking", "hillclimbing"],
            4: ["simulated annealing"],
        }

    def get_feedback(self, question_id, answer, user_answer, explanation=""):
        feedback = {}

        user_norm = str(user_answer).strip().lower()
        valid_answers = self.valid_strategies.get(question_id, [answer[0] if answer else ""])

        if answer is None or answer == (None, None):
            answer_str = "(raspunsuri generale: " + ", ".join(valid_answers) + ")"
        else:
            answer_str = f"{answer[0].lower()} ({answer[1]:.6f} sec) (raspunsuri generale: {', '.join(valid_answers)})"

        if user_norm in valid_answers:
            points = 100
            message = "Raspuns corect!"
        else:
            points = 0
            message = "Raspuns gresit. " + explanation

        feedback["points"] = points
        feedback["message"] = message
        feedback["correct_answer"] = answer_str

        return feedback
