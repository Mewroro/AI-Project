from AnswerCheckers.NashAnswerChecker import NashAnswerChecker
from Questions.NashQuestion import NashQuestion

def main():

    num_questions = int(input("Câte întrebări vrei să generezi? "))

    nash = NashQuestion()

    for i in range(num_questions):
        print(f"\nIntrebarea {i + 1}:")
        question_text, answer, matrix, player1_strategies, player2_strategies, explanation = nash.generate()
        print(question_text)

        user_answer = input("Raspunsul tău: ")
        nash_checker = NashAnswerChecker()

        feedback = nash_checker.get_nash_feedback(answer, user_answer, explanation)
        print(feedback["message"])
        print(feedback["points"])
        print(feedback["correct_answer"])

main()
