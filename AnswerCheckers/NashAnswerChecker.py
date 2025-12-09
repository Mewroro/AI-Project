import re

class NashAnswerChecker:
    PARTIAL_RESPONSE_THRESHOLD = 1

    def __init__(self):
        pass

    def get_nash_feedback(self, answer, user_answer, explanation):
        points = 0
        feedback = {}

        is_answer_int = False

        if type(answer) == int:
            is_answer_int = True
            points = self.check_count(answer, user_answer)
        elif type(answer) == list and len(answer) > 0 and type(answer[0]) == tuple:
            points = self.check_equilibria(answer, user_answer)
        elif type(answer) == list and len(answer) > 0 and  type(answer[0]) == str:
            points = self.check_dominant_strategies(answer, user_answer)
        elif type(answer) == list and len(answer) == 0:
            if user_answer.strip() == "0":
                points = 100
            else:
                points = 0

        if points == 100:
            feedback["message"] = "Raspuns corect!"
        elif points == 50:
            feedback["message"] = "Raspuns partial corect! " + explanation
        else:
            feedback["message"] = "Raspuns gresit. " + explanation

        if not is_answer_int and len(answer) == 0:
            answer = 0

        feedback["points"] = points
        feedback["correct_answer"] = answer

        return feedback

    def check_count(self, answer, user_answer):
        try:
            user_answer_value = int(user_answer)
        except:
            return 0

        if answer == user_answer_value:
            return 100

        if abs(answer - user_answer_value) <= self.PARTIAL_RESPONSE_THRESHOLD:
            return 50

        return 0

    def check_equilibria(self, answer, user_answer):
        user_answer = user_answer.upper().strip()

        pattern = r"\(\s*([A-Za-z0-9]+)\s*,\s*([A-Za-z0-9]+)\s*\)"
        matches = re.findall(pattern, user_answer)

        user_tuples = [(a, b) for a, b in matches]

        correct_set = set(answer)
        user_set = set(user_tuples)

        total_correct = len(correct_set)
        if total_correct == 0:
            return 0

        correctly_found = len(correct_set & user_set)
        points = int((correctly_found / total_correct) * 100)

        return points

    def check_dominant_strategies(self, answer, user_answer):
        user_answer = user_answer.upper().strip()

        user_list = user_answer.split()

        correct_set = set(answer)
        user_set = set(user_list)

        total_correct = len(correct_set)

        if total_correct == 0:
            return 0

        correctly_found = len(correct_set & user_set)
        points = int((correctly_found / total_correct) * 100)

        return points