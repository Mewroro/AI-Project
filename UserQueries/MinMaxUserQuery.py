import random
from Algorithms.MinMax import MinMax

class MinMaxUserQuery:
    def process(self, message: str):
        message = message.strip().lower()

        if "aleatoriu" in message:
            return self.handle_random_query(message)
        else:
            return self.handle_custom_tree(message)

    def handle_random_query(self, message: str):
        depth = random.randint(2, 4)
        leaf_count = random.randint(2 ** (depth - 1), 2 ** depth)
        leaf_values = [random.randint(-100, 100) for _ in range(leaf_count)]

        minmax_obj = MinMax(depth, leaf_values)
        question_type = self.detect_question(message)
        answer = self.compute_answer(minmax_obj, question_type)

        return {
            "depth": depth,
            "leaf_values": leaf_values,
            "answer": answer,
            "question_type": question_type
        }

    def handle_custom_tree(self, message: str):
        parsed = self.parse_custom_tree_input(message)
        if parsed is None:
            return "Format incorect. Exemplu: 3; 3,1,5,2; 2,2,2; Care va fi valoarea radacinii?"

        depth, leaf_values, structure, question = parsed

        minmax_obj = MinMax(depth, leaf_values)
        root = minmax_obj.build_tree_from_structure(leaf_values, structure)
        minmax_obj.tree = root

        question_type = self.detect_question(question)
        answer = self.compute_answer(minmax_obj, question_type)

        return {
            "depth": depth,
            "leaf_values": leaf_values,
            "structure": structure,
            "answer": answer,
            "question": question,
            "question_type": question_type
        }

    def parse_custom_tree_input(self, text: str):
        try:
            parts = [p.strip() for p in text.split(';')]
            if len(parts) < 4:
                return None

            depth = int(parts[0])
            leaf_values = [int(x) for x in parts[1].split(',')]
            structure = [int(x) for x in parts[2].split(',')]
            question = parts[3]

            return depth, leaf_values, structure, question
        except Exception:
            return None

    def detect_question(self, question: str):
        question = question.lower().strip()

        if "valoarea" in question and "radacinii" in question:
            return "root_value"

        if "numarul minim" in question or "frunze evaluate" in question:
            return "min_leaves"

        return None

    def compute_answer(self, minmax_obj, question_type: str):
        if question_type == "root_value":
            return minmax_obj.run_minmax()
        elif question_type == "min_leaves":
            minmax_obj.evaluated_leaves = 0
            minmax_obj.run_minmax()
            return minmax_obj.evaluated_leaves
        return None
