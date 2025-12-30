import random
import re

from Algorithms.Nash import Nash

class NashUserQuery:
    def process(self, message: str):
        message = message.strip().lower()

        if "aleatoriu" in message:
            return self.handle_random_query(message)

        return self.handle_manual_query(message)

    def handle_random_query(self, message):
        matrix, p1, p2 = self.generate_random_game()

        question_type = self.detect_question(message)
        if question_type is None:
            return "Nu recunosc tipul de întrebare."

        nash = Nash(matrix, p1, p2)
        nash.find_pure_nash()

        answer = self.compute_answer(nash, question_type)

        return {
            "matrix": matrix,
            "player1": p1,
            "player2": p2,
            "answer": answer,
            "question_type": question_type
        }

    def handle_manual_query(self, message):
        parsed = self.parse_manual_input(message)
        if parsed is None:
            return "Format incorect. Exemplu corect:\n" \
                   "[[(1,1) (2,2)] [(3,3) (2,1)]]; [A1, B1]; [A2, B2]; cate echilibre Nash pure?"

        matrix, p1, p2, question = parsed

        question_type = self.detect_question(question)
        if question_type is None:
            return "Nu recunosc tipul de întrebare."

        nash = Nash(matrix, p1, p2)
        nash.find_pure_nash()

        answer = self.compute_answer(nash, question_type)

        return {
            "matrix": matrix,
            "player1": p1,
            "player2": p2,
            "answer": answer,
            "question_type": question_type
        }

    def parse_manual_input(self, text):
        try:
            parts = [p.strip() for p in text.split(';')]
            if len(parts) < 4:
                return None

            matrix_raw = parts[0]
            p1_raw = parts[1]
            p2_raw = parts[2]
            question = parts[3]

            matrix = self.parse_matrix(matrix_raw)
            p1 = self.parse_strategies(p1_raw)
            p2 = self.parse_strategies(p2_raw)

            return matrix, p1, p2, question

        except:
            return None

    def parse_strategies(self, raw):
        return re.findall(r"[A-Za-z]+\d+", raw)

    def parse_matrix(self, raw):
        rows = re.findall(r"\[(.*?)\]", raw)
        matrix = []
        for r in rows:
            pairs = re.findall(r"\((-?\d+),\s*(-?\d+)\)", r)
            matrix.append([(int(a), int(b)) for a, b in pairs])
        return matrix

    def detect_question(self, question):
        question = question.lower().strip()

        if "cat" in question and "echilib" in question:
            return "count"

        if "care" in question and "echilibre" in question:
            return "list"

        if "strategiile dominante" in question and "1" in question:
            return "dom_p1"

        if "strategiile dominante" in question and "2" in question:
            return "dom_p2"

        return None

    def compute_answer(self, nash, question_type):
        if question_type == "count":
            return nash.equilibrium_count

        if question_type == "list":
            return nash.equilibria

        if question_type == "dom_p1":
            return nash.get_player1_dominant_strategies()

        if question_type == "dom_p2":
            return nash.get_player2_dominant_strategies()

        return None

    def generate_random_game(self):
        rows = random.randint(2, 4)
        cols = random.randint(2, 4)

        matrix = [
            [(random.randint(0, 10), random.randint(0, 10)) for _ in range(cols)]
            for _ in range(rows)
        ]

        p1 = [f"A{i + 1}" for i in range(rows)]
        p2 = [f"B{i + 1}" for i in range(cols)]

        return matrix, p1, p2
