class MinMaxAnswerChecker:
    ALPHA_BETA_PARTIAL_RESPONSE_THRESHOLD = 1
    DEPTH_PARTIAL_RESPONSE_THRESHOLD = 2

    def __init__(self):
        pass
    def get_minmax_feedback(self, answer, user_answer, explanation, question_id, minmax):
        feedback = {}
        points = 0

        if question_id == 1:
            points = self.check_root_value(answer, user_answer, minmax)

        elif question_id == 2:
            points = self.check_alpha_beta(answer, user_answer)

        if points == 100:
            feedback["message"] = "Răspuns corect!"
        elif points == 50:
            feedback["message"] = "Răspuns parțial corect! " + explanation
        else:
            feedback["message"] = "Răspuns greșit. " + explanation

        feedback["points"] = points
        feedback["correct_answer"] = answer

        return feedback

    def check_root_value(self, answer, user_answer, minmax):
        try:
            user_value = int(user_answer)
        except:
            return 0

        if user_value == answer:
            return 100
        elif minmax.get_depth_of_value(user_value) <= self.DEPTH_PARTIAL_RESPONSE_THRESHOLD:
            return 50
        return 0

    def check_alpha_beta(self, answer, user_answer):
        try:
            user_value = int(user_answer)
        except:
            return 0

        if user_value == answer:
            return 100

        if abs(user_value - answer) <= self.ALPHA_BETA_PARTIAL_RESPONSE_THRESHOLD:
            return 50

        return 0
