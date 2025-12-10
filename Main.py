from AnswerCheckers.NashAnswerChecker import NashAnswerChecker
from Questions.NashQuestion import NashQuestion
from UserQueries.NashUserQuery import NashUserQuery

def main():

    print("Alege modul:")
    print("1 - Generează întrebări random (sistemul tău standard)")
    print("2 - Lasă userul să pună întrebări despre algoritmul Nash")
    mode = input("Mod: ").strip()

    if mode == "1":
        num_questions = int(input("Câte întrebări vrei să generezi? "))

        nash = NashQuestion()

        for i in range(num_questions):
            print(f"\nIntrebarea {i + 1}:")
            question_text, answer, matrix, p1, p2, explanation = nash.generate()
            print(question_text)

            user_answer = input("Raspunsul tău: ")
            nash_checker = NashAnswerChecker()

            feedback = nash_checker.get_nash_feedback(answer, user_answer, explanation)
            print(feedback["message"])
            print("Puncte:", feedback["points"])
            print("Răspuns corect:", feedback["correct_answer"])

        return

    elif mode == "2":
        print("\nScrie întrebarea ta despre algoritmul Nash.")
        print("Exemple:")
        print("  aleatoriu, cate echilibre Nash pure?")
        print("  [[(1,1) (2,2)] [(3,3) (2,1)]], [A1, B1], [A2, B2], care sunt echilibrele Nash pure?")
        print("Scrie 'exit' pentru a ieși.")

        query = NashUserQuery()
        checker = NashAnswerChecker()

        while True:
            msg = input("\nÎntrebarea ta: ")

            if msg.lower().strip() == "exit":
                break

            result = query.process(msg)

            if isinstance(result, str):
                print("Eroare:", result)
                continue

            print("\nJocul este:")
            for r in result["matrix"]:
                print(r)

            print("Player1 strategies:", result["player1"])
            print("Player2 strategies:", result["player2"])
            print("Tip întrebare:", result["question_type"])
            print("Răspuns generat:", result["answer"])

        return

    else:
        print("Mod invalid!")

main()