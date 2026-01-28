from AnswerCheckers.CSPAnswerChecker import CSPAnswerChecker
from AnswerCheckers.MinMaxAnswerChecker import MinMaxAnswerChecker
from AnswerCheckers.NashAnswerChecker import NashAnswerChecker
from AnswerCheckers.SearchAnswerChecker import SearchAnswerChecker
from Questions.CSPQuestion import CSPQuestion
from Questions.MinMaxQuestion import MinMaxQuestion
from Questions.NashQuestion import NashQuestion
from Questions.SearchQuestion import SearchQuestion
from UserQueries.MinMaxUserQuery import MinMaxUserQuery
from UserQueries.NashUserQuery import NashUserQuery

def main():

    print("Alege modul:")
    print("1 - Genereaza intrebari Nash")
    print("2 - Genereaza întrebari MinMax")
    print("3 - Lasa userul sa puna intrebari despre algoritmul Nash")
    print("4 - Genereaza întrebari CSP")
    print("5 - Lasa userul sa puna intrebari despre algoritmul MinMax")
    print("6 - Genereaza întrebari Search")
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
        num_questions = int(input("Câte întrebări vrei să generezi? "))

        minmax_question = MinMaxQuestion()

        for i in range(num_questions):
            print(f"\nIntrebarea {i + 1}:")
            # ca sa iei tree-ul fa minmax.tree
            question_text, answer, minmax, question_id, explanation = minmax_question.generate()
            print(question_text)

            user_answer = input("Raspunsul tău: ")
            minmax_checker = MinMaxAnswerChecker()

            feedback = minmax_checker.get_minmax_feedback(answer, user_answer, explanation, question_id, minmax)
            print(feedback["message"])
            print("Puncte:", feedback["points"])
            print("Răspuns corect:", feedback["correct_answer"])

        return

    elif mode == "3":
        print("\nScrie întrebarea ta despre algoritmul Nash.")
        print("Exemple:")
        print("  aleatoriu, cate echilibre Nash pure?")
        print("  [[(1,1) (2,2)] [(3,3) (2,1)]]; [A1, B1]; [A2, B2]; care sunt echilibrele Nash pure?")
        print("Scrie 'exit' pentru a ieși.")

        query = NashUserQuery()

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

    elif mode == "4":
        num_questions = int(input("Cate întrebari CSP vrei sa generezi? "))

        csp_question = CSPQuestion()
        csp_checker = CSPAnswerChecker()

        for i in range(num_questions):
            print(f"\nIntrebarea CSP {i + 1}:")
            question_text, answer, explanation = csp_question.generate()

            print(question_text)

            user_answer = input("\nRaspunsul tau (ex: X=1 Y=2 sau 'nu exista solutie'): ")

            feedback = csp_checker.get_csp_feedback(answer, user_answer, explanation)

            print(feedback["message"])
            print("Puncte:", feedback["points"])
            print("Raspuns corect:", feedback["correct_answer"])

        return
    elif mode == "5":
        print("\nScrie intrebarea ta despre algoritmul MinMax.")
        print("Exemple:")
        print("  aleatoriu")
        print("  3; 3,1,5,2; 2,2,2; Care va fi valoarea radacinii?")
        print("Scrie 'exit' pentru a iesi.")

        query = MinMaxUserQuery()

        while True:
            msg = input("\nintrebarea ta: ")

            if msg.lower().strip() == "exit":
                break

            result = query.process(msg)

            if isinstance(result, str):
                print("Eroare:", result)
                continue

            print("\nDetalii arbore MinMax:")
            print("Adancime:", result["depth"])
            print("Valori frunze:", result["leaf_values"])
            if "structure" in result:
                print("Structura arborelui:", result["structure"])
            print("Intrebare:", result["question"])
            print(result["answer"])
    elif mode == "6":
        num_questions = int(input("Cate întrebari Search vrei sa generezi? "))

        search_question = SearchQuestion()
        search_checker = SearchAnswerChecker()

        for i in range(num_questions):
            print(f"\nIntrebarea Search {i + 1}:")
            question_text, answer, explanation = search_question.generate()

            print(question_text)

            user_answer = input("\nRaspunsul tau:")

            feedback = search_checker.get_feedback(answer, user_answer, explanation)

            print(feedback["message"])
            print("Puncte:", feedback["points"])
            print("Raspuns corect:", feedback["correct_answer"])
    else:
        print("Mod invalid!")

main()