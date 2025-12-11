import random
from Algorithms.MinMax import MinMax
from Questions.QuestionBase import QuestionBase


class MinMaxQuestion(QuestionBase):
    def __init__(self):
        super().__init__("minmax")
    def get_answer(self, id, minmax):
        minmax.run_minmax()
        if id == 1:
            return minmax.root_value

        if id == 2:
            return minmax.evaluated_leaves

        return None

    def generate(self):
        question = self.get_random_template()
        question_id = question["id"]
        template = question["template"]
        variables = question["vars"]
        explanation = question["explanation"]

        values = {}
        depth_value = None
        for var in variables:
            if var["name"] == "D":
                depth_value = random.randint(var["min-val"], var["max-val"])
                values["D"] = depth_value
                break

        for var in variables:
            if var["name"] != "N":
                continue

            leaves_min = var["min-val"]
            leaves_max = var["max-val"]

            count = random.randint(depth_value, depth_value**2)
            leaves = [random.randint(leaves_min, leaves_max) for _ in range(count)]
            values["N"] = leaves

        minmax = MinMax(depth_value, values["N"])
        answer = self.get_answer(question_id, minmax)

        question_text = template
        for k, v in values.items():
            if k == "N":
                string_list = ", ".join(str(x) for x in v)
                question_text = question_text.replace("{" + k + "}", string_list)
            elif k == "D":
                question_text = question_text.replace("{" + k + "}", str(v))
                explanation = explanation.replace("{" + k + "}", str(v))

        return question_text, answer, minmax, question_id, explanation
