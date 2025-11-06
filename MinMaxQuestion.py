import random

from MinMax import minimax, build_tree
from QuestionBase import QuestionBase

class MinimaxQuestion(QuestionBase):
    def __init__(self):
        super().__init__("minmax")

    def get_answer(self, template, values):
        tree = None
        counter = [0]

        if "radacina" in template:
            leaves = values["N"]
            tree = build_tree(leaves)
            answer = minimax(tree, 0, float('-inf'), float('inf'), True, counter)
        elif "alfa-beta" in template:
            leaves = values["N"]
            tree = build_tree(leaves)
            minimax(tree, 0, float('-inf'), float('inf'), True, counter)
            answer = counter[0]
        elif "cate noduri frunza" in template:
            answer = 2 ** values["D"]

        return answer, tree

    def generate(self):
        question = self.get_random_template()
        template = question["template"]
        variables = question["vars"]
        explanation_template = question["explanation"]

        values = {}
        for var in variables:
            name = var["name"]
            min_val = var["min-val"]
            max_val = var["max-val"]

            if "N" == name:
                depth = values["D"]
                leaves_count = 2 ** depth
                value = [random.randint(min_val, max_val) for _ in range(leaves_count)]
            else:
                value = random.randint(min_val, max_val)

            values[name] = value

        question_text = template
        for k, v in values.items():
            question_text = question_text.replace("{" + k + "}", str(v))

        answer, tree = self.get_answer(template, values)

        explanation = explanation_template
        for k, v in values.items():
            explanation = explanation.replace("{" + k + "}", str(v))

        if "{root_value}" in explanation:
            explanation = explanation.replace("{root_value}", str(answer))

        return question_text, answer, tree, explanation


