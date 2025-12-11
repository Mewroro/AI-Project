import tkinter as tk
from tkinter import ttk, messagebox

from AnswerCheckers.MinMaxAnswerChecker import MinMaxAnswerChecker
from Questions.MinMaxQuestion import MinMaxQuestion


class AIExamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generator Întrebări - Inteligență Artificială")
        self.geometry("1300x800")
        self.configure(bg="#f5f5f5")

        self.questions = []
        self.answers = {}
        self.trees = {}
        self.explanations = {}
        self.current_index = 0

        self.last_feedback = None
        self.last_tree = None
        self.last_explanation = None
        self.last_points = 0

        style = ttk.Style(self)
        style.configure("TLabel", font=("Arial", 14))
        style.configure("TButton", font=("Arial", 13), padding=8)
        style.configure("TCheckbutton", font=("Arial", 13))
        style.configure("TEntry", font=("Arial", 13))

        self.create_main_frame()

    # Pagina principală
    def create_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.main_frame = ttk.Frame(self, padding=30)
        self.main_frame.pack(fill="both", expand=True)

        ttk.Label(
            self.main_frame,
            text="🧠 Generator de întrebări - Inteligență Artificială",
            font=("Arial", 26, "bold"),
        ).pack(pady=30)

        ttk.Label(self.main_frame, text="Număr întrebări:", font=("Arial", 15)).pack(pady=5)
        self.num_questions = tk.IntVar(value=3)
        ttk.Entry(self.main_frame, textvariable=self.num_questions, width=10).pack()

        ttk.Label(self.main_frame, text="\nSelectează capitolele:", font=("Arial", 15, "bold")).pack(pady=(20, 10))

        self.chapters = {"MinMax": tk.BooleanVar()}
        chapters_frame = ttk.Frame(self.main_frame)
        chapters_frame.pack(pady=10)
        ttk.Checkbutton(chapters_frame, text="MinMax", variable=self.chapters["MinMax"]).pack(anchor="w", pady=3)

        ttk.Button(self.main_frame, text="✨ Generează întrebări", command=self.generate_questions).pack(pady=25)

    # Generare întrebări
    def generate_questions(self):
        num = self.num_questions.get()
        if not self.chapters["MinMax"].get():
            messagebox.showwarning("Atenție", "Selectează capitolul MinMax!")
            return

        minimax = MinMaxQuestion()
        self.questions, self.answers, self.trees, self.explanations = [], {}, {}, {}

        for i in range(num):
            q_text, answer, tree, explanation = minimax.generate()
            self.questions.append(q_text)
            self.answers[q_text] = answer
            self.trees[q_text] = tree
            self.explanations[q_text] = explanation

        self.current_index = 0
        self.show_questions_page()

    # Pagina de întrebări
    def show_questions_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.q_frame = ttk.Frame(self, padding=20)
        self.q_frame.pack(fill="both", expand=True)

        question_text = self.questions[self.current_index]
        ttk.Label(
            self.q_frame,
            text=question_text,
            wraplength=1000,
            font=("Arial", 18),
        ).pack(pady=20)

        # Canvas arbore doar dacă există
        self.tree_canvas = None
        if self.trees[self.questions[self.current_index]] is not None:
            self.tree_canvas = tk.Canvas(self.q_frame, width=1200, height=300, bg="white", relief="solid", bd=1)
            self.tree_canvas.pack_forget()

        self.answer_text = tk.Text(self.q_frame, height=8, width=120, font=("Arial", 13))
        self.answer_text.pack(pady=15)

        button_frame = ttk.Frame(self.q_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="✅ Evaluează răspuns", command=self.evaluate_answer).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="➡️ Următoarea întrebare", command=self.next_question).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="⬅️ Înapoi", command=self.back_to_main).grid(row=0, column=2, padx=10)

    # Desen arbore
    def draw_tree(self, root):
        levels = self.get_levels(root)
        canvas_width = 1200
        node_radius = 20
        vertical_gap = 70

        self.tree_canvas.config(width=canvas_width, height=max(300, len(levels)*vertical_gap + 50))
        self.tree_canvas.delete("all")

        positions = {}  # pozițiile nodurilor pentru linii
        for depth, nodes in enumerate(levels):
            y = 50 + depth * vertical_gap
            total = len(nodes)
            for i, node in enumerate(nodes):
                x = int(canvas_width / (total + 1) * (i + 1))
                positions[node] = (x, y)

                # desen nod
                self.tree_canvas.create_oval(x - node_radius, y - node_radius,
                                             x + node_radius, y + node_radius,
                                             fill="#e0f7fa")
                self.tree_canvas.create_text(x, y, text=str(node.value), font=("Arial", 10))

                # desen linie către părinte
                for parent in positions:
                    if parent.left == node or parent.right == node:
                        px, py = positions[parent]
                        self.tree_canvas.create_line(px, py + node_radius, x, y - node_radius, fill="gray")

    # Obțin nivelele arborelui
    def get_levels(self, root):
        if not root:
            return []
        levels = []
        current_level = [root]
        while current_level:
            levels.append(current_level)
            next_level = []
            for node in current_level:
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            current_level = next_level
        return levels

    # Evaluare răspuns
    def evaluate_answer(self):
        user_answer = self.answer_text.get("1.0", "end").strip()
        q = self.questions[self.current_index]

        feedback = MinMaxAnswerChecker.get_minmax_feedback(
            self.answers[q], user_answer, self.trees[q], self.explanations[q]
        )

        points = feedback.get("points", 0)
        msg = feedback["message"]
        if "correct_answer" in feedback:
            msg += f"\n\nRăspuns corect: {feedback['correct_answer']}"
        msg += f"\n📊 Scor: {points}/100"

        messagebox.showinfo("Evaluare răspuns", msg)

        # Salvăm date pentru explicația completă
        self.last_feedback = feedback
        self.last_tree = self.trees[q]
        self.last_explanation = self.explanations[q]
        self.last_points = points

        ttk.Button(self.q_frame, text="📘 Arată explicația completă",
                   command=self.show_full_explanation).pack(pady=10)

    # Explicație completă + arbore
    def show_full_explanation(self):
        if self.last_tree is not None:
            self.tree_canvas.pack(pady=10)
            self.draw_tree(self.last_tree)

        ttk.Label(
            self.q_frame,
            text=f"📊 Punctaj: {self.last_points}/100\n\n🔍 Explicație:\n{self.last_explanation}",
            wraplength=1000,
            font=("Arial", 13, "italic"),
            foreground="#222",
            justify="left"
        ).pack(pady=10)

    # Trecere la următoarea întrebare
    def next_question(self):
        self.current_index += 1
        if self.current_index >= len(self.questions):
            messagebox.showinfo("Gata!", "Ai terminat toate întrebările ✅")
            self.back_to_main()
        else:
            self.show_questions_page()

    def back_to_main(self):
        self.current_index = 0
        self.create_main_frame()


if __name__ == "__main__":
    app = AIExamApp()
    app.mainloop()
