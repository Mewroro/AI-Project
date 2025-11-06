from MinMax import get_final_tree_values

class CheckAnswer:
    def __init__(self):
        pass

    @staticmethod
    def _is_power_of_two(n):
        if not isinstance(n, int) or n <= 0:
            return False
        return (n & (n - 1)) == 0
    @staticmethod
    def get_minmax_feedback(answer, user_answer, tree, explanation):
        feedback = {}
        full_points = 100
        partial_points = 0

        user_answer = user_answer.split()

        for word in user_answer:
            if str(word) == str(answer):
                feedback["message"] = "Raspuns corect!"
                feedback["points"] = full_points
                return feedback

        # este pentru adancimea minima
        if tree is None:
            if CheckAnswer._is_power_of_two(answer):
                feedback["message"] = "Raspuns partial corect!"
                partial_points = 50
            else:
                feedback["message"] = "Raspuns gresit!"

            feedback["points"] = partial_points
            feedback["correct_answer"] = answer
            return feedback


        final_values = get_final_tree_values(tree)

        final_values_numeric = [v for v in final_values if v != "None"]

        if user_answer in final_values_numeric:
            feedback["message"] = "Raspuns partial corect! "
            partial_points = 0.5
        else:
            feedback["message"] = "Raspuns gresit. "

        feedback["message"] += explanation
        feedback["points"] = partial_points
        feedback["correct_answer"] = answer

        return feedback