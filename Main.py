import MinMax
from CheckAnswer import CheckAnswer
from MinMaxQuestion import MinimaxQuestion

def main():

    num_questions = int(input("Câte întrebări vrei să generezi? "))

    minimax = MinimaxQuestion()

    for i in range(num_questions):
        print(f"\nIntrebarea {i + 1}:")
        question_text, answer, tree, explanation = minimax.generate()
        print(question_text)

        user_answer = input("Raspunsul tău: ")
        print(user_answer)

        feedback = CheckAnswer.get_minmax_feedback(answer, user_answer, tree, explanation)

        if feedback["points"] != 100:
            if tree is not None:
                MinMax.print_final_tree(tree)
            print(feedback["message"] + " Raspuns corect: " + str(feedback["correct_answer"]) + ". Scor:" + str(feedback["points"]) + "/100")
            continue

        print(feedback["message"] + "Scor:" + str(feedback["points"]) + "/100")

main()
