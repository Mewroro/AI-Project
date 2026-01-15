class SearchAnswerChecker:
    def __init__(self):
        pass

    def get_feedback(self, answer, user_answer, explanation=""):
        feedback = {}

        user_norm = str(user_answer).strip().lower()
        answer_str = f"{answer[0].lower()}"

        if user_norm in answer_str:
            points = 100
            message = "Raspuns corect!"
        else:
            points = 0
            message = "Raspuns gresit. " + explanation

        feedback["points"] = points
        feedback["message"] = message
        feedback["correct_answer"] = answer_str

        return feedback
