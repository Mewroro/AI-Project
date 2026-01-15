import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext

# ===== Backend imports (structura ta) =====
from Questions.MinMaxQuestion import MinMaxQuestion
from Questions.NashQuestion import NashQuestion
from Questions.CSPQuestion import CSPQuestion
from Questions.SearchQuestion import SearchQuestion

from AnswerCheckers.MinMaxAnswerChecker import MinMaxAnswerChecker
from AnswerCheckers.NashAnswerChecker import NashAnswerChecker
from AnswerCheckers.CSPAnswerChecker import CSPAnswerChecker
from AnswerCheckers.SearchAnswerChecker import SearchAnswerChecker

from UserQueries.NashUserQuery import NashUserQuery
from UserQueries.MinMaxUserQuery import MinMaxUserQuery


class AIExamUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Exam Trainer")
        self.geometry("1300x820")
        self.minsize(1100, 700)

        # ===== Theme =====
        self.theme = "light"
        self.colors = {
            "light": {
                "bg": "#f5f6f8",
                "card": "#ffffff",
                "text": "#111827",
                "muted": "#6b7280",
                "sidebar": "#ffffff",
                "sidebar_border": "#e5e7eb",
                "accent": "#2563eb",
                "accent_text": "#ffffff",
                "border": "#e5e7eb",
                "input_bg": "#ffffff",
                "canvas_bg": "#ffffff",
                "danger": "#ef4444",
                "success": "#16a34a",
            },
            "dark": {
                "bg": "#0b1220",
                "card": "#111827",
                "text": "#f9fafb",
                "muted": "#9ca3af",
                "sidebar": "#0f172a",
                "sidebar_border": "#1f2937",
                "accent": "#3b82f6",
                "accent_text": "#0b1220",
                "border": "#1f2937",
                "input_bg": "#0b1220",
                "canvas_bg": "#0b1220",
                "danger": "#f87171",
                "success": "#4ade80",
            }
        }

        # ===== App state for pages =====
        self.state = {
            "minmax": {"items": [], "idx": 0},
            "nash": {"items": [], "idx": 0},
            "csp": {"items": [], "idx": 0},
            "search": {"items": [], "idx": 0},
        }

        self._setup_ttk_style()
        self._build_shell()
        self.apply_theme()
        self.show_page("home")

    # ------------------------------------------------------------------
    # STYLE / THEME
    # ------------------------------------------------------------------
    def _setup_ttk_style(self):
        style = ttk.Style(self)
        for th in ("clam", "vista", "xpnative", "alt"):
            try:
                style.theme_use(th)
                break
            except:
                pass

        style.configure("TLabel", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 11), padding=8)
        style.configure("TEntry", font=("Segoe UI", 11))
        style.configure("TCheckbutton", font=("Segoe UI", 11))

    def apply_theme(self):
        c = self.colors[self.theme]
        self.configure(bg=c["bg"])

        self.header.configure(bg=c["bg"])
        self.sidebar.configure(bg=c["sidebar"])
        self.sidebar_border.configure(bg=c["sidebar_border"])
        self.content_container.configure(bg=c["bg"])

        # header labels/buttons
        self.header_title.configure(bg=c["bg"], fg=c["text"])
        self.theme_btn.configure(
            bg=c["accent"], fg=c["accent_text"],
            activebackground=c["accent"], activeforeground=c["accent_text"],
            bd=0, highlightthickness=0
        )

        # sidebar buttons
        for b in self.sidebar_buttons:
            b.configure(
                bg=c["sidebar"], fg=c["text"],
                activebackground=c["border"], activeforeground=c["text"],
                bd=0, highlightthickness=0
            )
        for lbl in self.sidebar_labels:
            lbl.configure(bg=c["sidebar"], fg=c["muted"])

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()
        self.show_page(self.current_page)  # redraw

    # ------------------------------------------------------------------
    # SHELL LAYOUT (HEADER + SIDEBAR + SCROLLABLE CONTENT)
    # ------------------------------------------------------------------
    def _build_shell(self):
        c = self.colors[self.theme]

        # Header
        self.header = tk.Frame(self, bg=c["bg"], height=56)
        self.header.pack(side="top", fill="x")

        self.header_title = tk.Label(
            self.header, text="AI Exam Trainer",
            font=("Segoe UI", 18, "bold"),
            bg=c["bg"], fg=c["text"]
        )
        self.header_title.pack(side="left", padx=16, pady=10)

        self.theme_btn = tk.Button(
            self.header, text="Toggle Light/Dark",
            command=self.toggle_theme,
            font=("Segoe UI", 10, "bold"),
            padx=12, pady=8
        )
        self.theme_btn.pack(side="right", padx=14, pady=10)

        # Main
        main = tk.Frame(self, bg=c["bg"])
        main.pack(side="top", fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(main, bg=c["sidebar"], width=260)
        self.sidebar.pack(side="left", fill="y")

        self.sidebar_border = tk.Frame(main, bg=c["sidebar_border"], width=1)
        self.sidebar_border.pack(side="left", fill="y")

        # Content container (we recreate scrollable content each page)
        self.content_container = tk.Frame(main, bg=c["bg"])
        self.content_container.pack(side="left", fill="both", expand=True)

        # Sidebar items
        self.sidebar_buttons = []
        self.sidebar_labels = []

        def add_section(title):
            lbl = tk.Label(self.sidebar, text=title, font=("Segoe UI", 11, "bold"),
                           bg=c["sidebar"], fg=c["muted"])
            lbl.pack(anchor="w", padx=16, pady=(18, 6))
            self.sidebar_labels.append(lbl)

        def add_btn(text, page_key):
            b = tk.Button(
                self.sidebar, text=text, anchor="w",
                command=lambda: self.show_page(page_key),
                font=("Segoe UI", 11),
                padx=16, pady=10
            )
            b.pack(fill="x", padx=10, pady=3)
            self.sidebar_buttons.append(b)

        add_section("Generare")
        add_btn("MinMax", "minmax")
        add_btn("Nash", "nash")
        add_btn("CSP", "csp")
        add_btn("Search", "search")

        add_section("Întrebări utilizator")
        add_btn("Întreabă MinMax", "ask_minmax")
        add_btn("Întreabă Nash", "ask_nash")

        add_section("Acasă")
        add_btn("Home", "home")

    # ------------------------------------------------------------------
    # SCROLLABLE RIGHT CONTENT
    # ------------------------------------------------------------------
    def _clear_content_container(self):
        for w in self.content_container.winfo_children():
            w.destroy()

    def _make_scrollable_right(self):
        """
        Creates a scrollable frame in content_container and returns 'inner' frame.
        """
        c = self.colors[self.theme]

        container = tk.Frame(self.content_container, bg=c["bg"])
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=c["bg"], highlightthickness=0)
        vbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)

        vbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=c["bg"])
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)

        def on_inner_configure(_event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_canvas_configure)
        inner.bind("<Configure>", on_inner_configure)

        # Mousewheel
        def _on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                # Linux
                if event.num == 4:
                    canvas.yview_scroll(-3, "units")
                elif event.num == 5:
                    canvas.yview_scroll(3, "units")

        # Bind to canvas only (avoid global bind_all issues when switching pages)
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)

        self._scroll_canvas = canvas
        self._scroll_inner = inner
        return inner

    # ------------------------------------------------------------------
    # UI HELPERS
    # ------------------------------------------------------------------
    def page_title(self, parent, title, subtitle=None):
        c = self.colors[self.theme]
        wrap = tk.Frame(parent, bg=c["bg"])
        wrap.pack(fill="x", padx=18, pady=(18, 6))
        tk.Label(wrap, text=title, bg=c["bg"], fg=c["text"],
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(wrap, text=subtitle, bg=c["bg"], fg=c["muted"],
                     font=("Segoe UI", 11)).pack(anchor="w", pady=(4, 0))

    def card(self, parent, title=None, subtitle=None):
        c = self.colors[self.theme]
        frame = tk.Frame(parent, bg=c["card"], bd=1, relief="solid", highlightthickness=0)
        frame.configure(highlightbackground=c["border"], highlightcolor=c["border"])
        frame.pack(fill="x", padx=18, pady=10)

        if title:
            tk.Label(frame, text=title, bg=c["card"], fg=c["text"],
                     font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=14, pady=(12, 4))
        if subtitle:
            tk.Label(frame, text=subtitle, bg=c["card"], fg=c["muted"],
                     font=("Segoe UI", 11)).pack(anchor="w", padx=14, pady=(0, 10))
        return frame

    def primary_button(self, parent, text, command):
        c = self.colors[self.theme]
        return tk.Button(
            parent, text=text, command=command,
            bg=c["accent"], fg=c["accent_text"],
            activebackground=c["accent"], activeforeground=c["accent_text"],
            padx=14, pady=8, bd=0, highlightthickness=0
        )

    def ghost_button(self, parent, text, command):
        c = self.colors[self.theme]
        return tk.Button(
            parent, text=text, command=command,
            bg=c["border"], fg=c["text"],
            activebackground=c["border"], activeforeground=c["text"],
            padx=14, pady=8, bd=0, highlightthickness=0
        )

    # ------------------------------------------------------------------
    # ROUTER
    # ------------------------------------------------------------------
    def show_page(self, key):
        self.current_page = key
        self._clear_content_container()
        parent = self._make_scrollable_right()

        if key == "home":
            self.page_home(parent)
        elif key == "minmax":
            self.page_minmax(parent)
        elif key == "nash":
            self.page_nash(parent)
        elif key == "csp":
            self.page_csp(parent)
        elif key == "search":
            self.page_search(parent)
        elif key == "ask_nash":
            self.page_ask_nash(parent)
        elif key == "ask_minmax":
            self.page_ask_minmax(parent)
        else:
            self.page_home(parent)

    # ------------------------------------------------------------------
    # HOME
    # ------------------------------------------------------------------
    def page_home(self, parent):
        c = self.colors[self.theme]
        self.page_title(parent, "Bun venit 👋", "Alege un modul din meniul din stânga.")
        info = self.card(parent, "Ce face aplicația", "Pe scurt:")
        txt = (
            "• Generează întrebări: MinMax / Nash / CSP / Search.\n"
            "• Evaluează răspunsul: punctaj + răspuns corect + feedback.\n"
            "• MinMax: afișează arborele gol (doar frunze) împreună cu enunțul.\n"
            "• Conținutul este scrollabil (nu se mai taie în ecran).\n"
            "• Toggle Light/Dark sus dreapta."
        )
        tk.Label(info, text=txt, bg=c["card"], fg=c["text"], justify="left",
                 font=("Segoe UI", 11)).pack(anchor="w", padx=14, pady=(0, 12))

    # ------------------------------------------------------------------
    # MINMAX
    # ------------------------------------------------------------------
    def page_minmax(self, parent):
        c = self.colors[self.theme]
        self.page_title(parent, "MinMax — Generare & Evaluare",
                        "Arborele gol (doar frunzele) apare imediat sub enunț.")

        controls = self.card(parent, "Setări", "Generează un set de întrebări MinMax.")
        row = tk.Frame(controls, bg=c["card"])
        row.pack(fill="x", padx=14, pady=(0, 12))

        tk.Label(row, text="Număr întrebări:", bg=c["card"], fg=c["text"],
                 font=("Segoe UI", 11)).pack(side="left")

        self.minmax_count = tk.StringVar(value="3")
        tk.Entry(row, textvariable=self.minmax_count, width=6,
                 bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]).pack(side="left", padx=10)

        self.primary_button(row, "Generează", self._minmax_generate).pack(side="left", padx=10)

        self.minmax_area = tk.Frame(parent, bg=c["bg"])
        self.minmax_area.pack(fill="both", expand=True)

        self._minmax_render()

    def _minmax_generate(self):
        try:
            n = int(self.minmax_count.get())
            if n <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Atenție", "Introduce un număr valid (>0).")
            return

        qgen = MinMaxQuestion()
        items = []
        for _ in range(n):
            q_text, answer, minmax_obj, qid, explanation = qgen.generate()
            tree = getattr(minmax_obj, "tree", None)
            items.append({
                "q": q_text,
                "answer": answer,
                "minmax": minmax_obj,
                "qid": qid,
                "explanation": explanation,
                "tree": tree,
                "feedback": None
            })

        self.state["minmax"]["items"] = items
        self.state["minmax"]["idx"] = 0
        self._minmax_render()

    def _minmax_render(self):
        c = self.colors[self.theme]
        for w in self.minmax_area.winfo_children():
            w.destroy()

        items = self.state["minmax"]["items"]
        idx = self.state["minmax"]["idx"]

        if not items:
            card = self.card(self.minmax_area, "Întrebări", "Generează întrebări ca să începi.")
            tk.Label(card, text="Apasă „Generează” din setări.",
                     bg=c["card"], fg=c["muted"]).pack(anchor="w", padx=14, pady=(0, 12))
            return

        item = items[idx]

        qcard = self.card(self.minmax_area, f"Întrebarea {idx+1}/{len(items)}", None)
        tk.Label(qcard, text=item["q"], bg=c["card"], fg=c["text"],
                 font=("Segoe UI", 12), wraplength=980, justify="left").pack(anchor="w", padx=14, pady=(0, 10))

        # Tree shown with statement
        if item["tree"] is not None:
            canvas_frame = tk.Frame(qcard, bg=c["card"])
            canvas_frame.pack(fill="x", padx=14, pady=(6, 12))

            # scrollable canvas (horizontal + vertical) for big trees
            canvas = tk.Canvas(canvas_frame, width=1040, height=260,
                               bg=c["canvas_bg"], highlightthickness=1,
                               highlightbackground=c["border"])
            hbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
            vbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
            canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

            canvas.grid(row=0, column=0, sticky="nsew")
            vbar.grid(row=0, column=1, sticky="ns")
            hbar.grid(row=1, column=0, sticky="ew")
            canvas_frame.grid_columnconfigure(0, weight=1)

            self._draw_minmax_empty_tree(canvas, item["tree"])

        ans_card = self.card(self.minmax_area, "Răspuns", "Introdu răspunsul tău și apasă Evaluează.")
        self.minmax_answer = tk.StringVar()
        tk.Entry(ans_card, textvariable=self.minmax_answer, width=50,
                 bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]).pack(anchor="w", padx=14, pady=(0, 10))

        btn_row = tk.Frame(ans_card, bg=c["card"])
        btn_row.pack(fill="x", padx=14, pady=(0, 12))

        self.primary_button(btn_row, "✅ Evaluează", self._minmax_evaluate).pack(side="left")
        self.ghost_button(btn_row, "📘 Explicație", self._minmax_show_explanation).pack(side="left", padx=10)
        self.ghost_button(btn_row, "⬅️ Înapoi", self._minmax_prev).pack(side="right")
        self.ghost_button(btn_row, "➡️ Următoarea", self._minmax_next).pack(side="right", padx=10)

        if item.get("feedback"):
            fb = item["feedback"]
            res = self.card(self.minmax_area, "Rezultat", None)
            tk.Label(res, text=f"Scor: {fb.get('points', 0)}/100",
                     bg=c["card"], fg=c["text"],
                     font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(0, 6))
            tk.Label(res, text=fb.get("message", ""), bg=c["card"], fg=c["text"],
                     wraplength=980, justify="left").pack(anchor="w", padx=14, pady=(0, 8))
            tk.Label(res, text=f"Răspuns corect: {fb.get('correct_answer', '')}",
                     bg=c["card"], fg=c["text"]).pack(anchor="w", padx=14, pady=(0, 12))

    def _minmax_evaluate(self):
        items = self.state["minmax"]["items"]
        idx = self.state["minmax"]["idx"]
        if not items:
            return
        item = items[idx]

        checker = MinMaxAnswerChecker()
        user = self.minmax_answer.get().strip()
        fb = checker.get_minmax_feedback(item["answer"], user, item["explanation"], item["qid"], item["minmax"])
        item["feedback"] = fb
        self._minmax_render()

    def _minmax_show_explanation(self):
        items = self.state["minmax"]["items"]
        idx = self.state["minmax"]["idx"]
        if not items:
            return
        item = items[idx]
        fb = item.get("feedback") or {"points": 0}
        explanation = item.get("explanation", "")
        messagebox.showinfo("Explicație", f"📊 Punctaj: {fb.get('points', 0)}/100\n\n🔍 Explicație:\n{explanation}")

    def _minmax_prev(self):
        if self.state["minmax"]["idx"] > 0:
            self.state["minmax"]["idx"] -= 1
            self._minmax_render()

    def _minmax_next(self):
        items = self.state["minmax"]["items"]
        if not items:
            return
        if self.state["minmax"]["idx"] < len(items) - 1:
            self.state["minmax"]["idx"] += 1
            self._minmax_render()
        else:
            messagebox.showinfo("Gata", "Ai ajuns la finalul setului de întrebări MinMax ✅")

    # ----- MinMax tree (N-ary) only leaves have values, MAX/MIN labels per level -----
    def _get_levels_nary(self, root):
        if root is None:
            return []
        levels = []
        current = [root]
        while True:
            real = [n for n in current if n is not None]
            if not real:
                break
            levels.append(real)
            nxt = []
            for n in real:
                children = getattr(n, "children", [])
                if children:
                    nxt.extend(children)
            current = nxt
        return levels

    def _draw_minmax_empty_tree(self, canvas, root):
        c = self.colors[self.theme]
        canvas.delete("all")

        levels = self._get_levels_nary(root)
        if not levels:
            canvas.create_text(20, 20, anchor="nw", text="(Arbore gol)", fill=c["muted"])
            return

        # X positions: assign leaves sequentially, internal centered above children
        positions = {}
        x_cursor = 90
        leaf_spacing = 70

        def assign(node):
            nonlocal x_cursor
            children = getattr(node, "children", [])
            if not children:
                positions[node] = x_cursor
                x_cursor += leaf_spacing
                return positions[node]
            xs = []
            for ch in children:
                xs.append(assign(ch))
            positions[node] = int(sum(xs) / len(xs))
            return positions[node]

        assign(root)

        node_r = 18
        level_gap = 75
        top = 35

        width_needed = max(1100, x_cursor + 120)
        height_needed = top + level_gap * len(levels) + 80
        canvas.configure(scrollregion=(0, 0, width_needed, height_needed))

        for depth, nodes in enumerate(levels):
            y = top + depth * level_gap
            label = "MAX" if depth % 2 == 0 else "MIN"
            canvas.create_text(14, y, anchor="w", text=label, fill=c["muted"], font=("Segoe UI", 10, "bold"))

            for node in nodes:
                x = positions.get(node, 90)
                children = getattr(node, "children", [])

                # lines to children
                for ch in children:
                    cx = positions.get(ch, x)
                    cy = top + (depth + 1) * level_gap
                    canvas.create_line(x, y + node_r, cx, cy - node_r, fill="#888")

                is_leaf = len(children) == 0
                outline = c["border"] if self.theme == "light" else "#334155"
                if self.theme == "light":
                    fill = "#e8f5e9" if is_leaf else c["card"]
                else:
                    fill = "#1f3d2b" if is_leaf else c["card"]

                canvas.create_oval(x - node_r, y - node_r, x + node_r, y + node_r,
                                   fill=fill, outline=outline, width=2)
                if is_leaf:
                    canvas.create_text(x, y, text=str(getattr(node, "value", "")),
                                       fill=c["text"], font=("Segoe UI", 10, "bold"))

    # ------------------------------------------------------------------
    # NASH
    # ------------------------------------------------------------------
    def page_nash(self, parent):
        c = self.colors[self.theme]
        self.page_title(parent, "Nash — Generare & Evaluare",
                        "Întrebarea include matricea în text (afișăm direct question_text).")

        controls = self.card(parent, "Setări", "Generează un set de întrebări Nash.")
        row = tk.Frame(controls, bg=c["card"])
        row.pack(fill="x", padx=14, pady=(0, 12))

        tk.Label(row, text="Număr întrebări:", bg=c["card"], fg=c["text"],
                 font=("Segoe UI", 11)).pack(side="left")

        self.nash_count = tk.StringVar(value="3")
        tk.Entry(row, textvariable=self.nash_count, width=6,
                 bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]).pack(side="left", padx=10)

        self.primary_button(row, "Generează", self._nash_generate).pack(side="left", padx=10)

        self.nash_area = tk.Frame(parent, bg=c["bg"])
        self.nash_area.pack(fill="both", expand=True)

        self._nash_render()

    def _nash_generate(self):
        try:
            n = int(self.nash_count.get())
            if n <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Atenție", "Introduce un număr valid (>0).")
            return

        qgen = NashQuestion()
        items = []
        for _ in range(n):
            q_text, answer, matrix, p1, p2, explanation = qgen.generate()
            items.append({
                "q": q_text,
                "answer": answer,
                "explanation": explanation,
                "feedback": None
            })

        self.state["nash"]["items"] = items
        self.state["nash"]["idx"] = 0
        self._nash_render()

    def _nash_render(self):
        c = self.colors[self.theme]
        for w in self.nash_area.winfo_children():
            w.destroy()

        items = self.state["nash"]["items"]
        idx = self.state["nash"]["idx"]
        if not items:
            card = self.card(self.nash_area, "Întrebări", "Generează întrebări ca să începi.")
            tk.Label(card, text="Apasă „Generează” din setări.",
                     bg=c["card"], fg=c["muted"]).pack(anchor="w", padx=14, pady=(0, 12))
            return

        item = items[idx]

        qcard = self.card(self.nash_area, f"Întrebarea {idx+1}/{len(items)}", None)
        tk.Label(qcard, text=item["q"], bg=c["card"], fg=c["text"],
                 font=("Segoe UI", 12), wraplength=980, justify="left").pack(anchor="w", padx=14, pady=(0, 10))

        ans_card = self.card(self.nash_area, "Răspuns", "Introdu răspunsul tău și apasă Evaluează.")
        self.nash_answer = tk.StringVar()
        tk.Entry(ans_card, textvariable=self.nash_answer, width=60,
                 bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]).pack(anchor="w", padx=14, pady=(0, 10))

        btn_row = tk.Frame(ans_card, bg=c["card"])
        btn_row.pack(fill="x", padx=14, pady=(0, 12))

        self.primary_button(btn_row, "✅ Evaluează", self._nash_evaluate).pack(side="left")
        self.ghost_button(btn_row, "📘 Explicație", self._nash_show_explanation).pack(side="left", padx=10)
        self.ghost_button(btn_row, "⬅️ Înapoi", self._nash_prev).pack(side="right")
        self.ghost_button(btn_row, "➡️ Următoarea", self._nash_next).pack(side="right", padx=10)

        if item.get("feedback"):
            fb = item["feedback"]
            res = self.card(self.nash_area, "Rezultat", None)
            tk.Label(res, text=f"Scor: {fb.get('points', 0)}/100",
                     bg=c["card"], fg=c["text"],
                     font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(0, 6))
            tk.Label(res, text=fb.get("message", ""), bg=c["card"], fg=c["text"],
                     wraplength=980, justify="left").pack(anchor="w", padx=14, pady=(0, 8))
            tk.Label(res, text=f"Răspuns corect: {fb.get('correct_answer', '')}",
                     bg=c["card"], fg=c["text"]).pack(anchor="w", padx=14, pady=(0, 12))

    def _nash_evaluate(self):
        items = self.state["nash"]["items"]
        idx = self.state["nash"]["idx"]
        if not items:
            return
        item = items[idx]
        checker = NashAnswerChecker()
        user = self.nash_answer.get().strip()
        fb = checker.get_nash_feedback(item["answer"], user, item["explanation"])
        item["feedback"] = fb
        self._nash_render()

    def _nash_show_explanation(self):
        items = self.state["nash"]["items"]
        idx = self.state["nash"]["idx"]
        if not items:
            return
        item = items[idx]
        fb = item.get("feedback") or {"points": 0}
        messagebox.showinfo("Explicație", f"📊 Punctaj: {fb.get('points', 0)}/100\n\n🔍 Explicație:\n{item.get('explanation','')}")

    def _nash_prev(self):
        if self.state["nash"]["idx"] > 0:
            self.state["nash"]["idx"] -= 1
            self._nash_render()

    def _nash_next(self):
        items = self.state["nash"]["items"]
        if not items:
            return
        if self.state["nash"]["idx"] < len(items) - 1:
            self.state["nash"]["idx"] += 1
            self._nash_render()
        else:
            messagebox.showinfo("Gata", "Ai ajuns la finalul setului de întrebări Nash ✅")

    # ------------------------------------------------------------------
    # CSP
    # ------------------------------------------------------------------
    def page_csp(self, parent):
        c = self.colors[self.theme]
        self.page_title(parent, "CSP — Generare & Evaluare", None)

        controls = self.card(parent, "Setări", "Generează un set de întrebări CSP.")
        row = tk.Frame(controls, bg=c["card"])
        row.pack(fill="x", padx=14, pady=(0, 12))

        tk.Label(row, text="Număr întrebări:", bg=c["card"], fg=c["text"],
                 font=("Segoe UI", 11)).pack(side="left")

        self.csp_count = tk.StringVar(value="3")
        tk.Entry(row, textvariable=self.csp_count, width=6,
                 bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]).pack(side="left", padx=10)

        self.primary_button(row, "Generează", self._csp_generate).pack(side="left", padx=10)

        self.csp_area = tk.Frame(parent, bg=c["bg"])
        self.csp_area.pack(fill="both", expand=True)

        self._csp_render()

    def _csp_generate(self):
        try:
            n = int(self.csp_count.get())
            if n <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Atenție", "Introduce un număr valid (>0).")
            return

        qgen = CSPQuestion()
        items = []
        for _ in range(n):
            q_text, answer, explanation = qgen.generate()
            items.append({"q": q_text, "answer": answer, "explanation": explanation, "feedback": None})

        self.state["csp"]["items"] = items
        self.state["csp"]["idx"] = 0
        self._csp_render()

    def _csp_render(self):
        c = self.colors[self.theme]
        for w in self.csp_area.winfo_children():
            w.destroy()

        items = self.state["csp"]["items"]
        idx = self.state["csp"]["idx"]
        if not items:
            card = self.card(self.csp_area, "Întrebări", "Generează întrebări ca să începi.")
            tk.Label(card, text="Apasă „Generează” din setări.",
                     bg=c["card"], fg=c["muted"]).pack(anchor="w", padx=14, pady=(0, 12))
            return

        item = items[idx]
        qcard = self.card(self.csp_area, f"Întrebarea {idx+1}/{len(items)}", None)
        tk.Label(qcard, text=item["q"], bg=c["card"], fg=c["text"],
                 wraplength=980, justify="left").pack(anchor="w", padx=14, pady=(0, 10))

        ans_card = self.card(self.csp_area, "Răspuns", "Ex: X=1 Y=2 sau 'nu exista solutie'")
        self.csp_answer = tk.StringVar()
        tk.Entry(ans_card, textvariable=self.csp_answer, width=60,
                 bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]).pack(anchor="w", padx=14, pady=(0, 10))

        btn_row = tk.Frame(ans_card, bg=c["card"])
        btn_row.pack(fill="x", padx=14, pady=(0, 12))

        self.primary_button(btn_row, "✅ Evaluează", self._csp_evaluate).pack(side="left")
        self.ghost_button(btn_row, "📘 Explicație", self._csp_show_explanation).pack(side="left", padx=10)
        self.ghost_button(btn_row, "⬅️ Înapoi", self._csp_prev).pack(side="right")
        self.ghost_button(btn_row, "➡️ Următoarea", self._csp_next).pack(side="right", padx=10)

        if item.get("feedback"):
            fb = item["feedback"]
            res = self.card(self.csp_area, "Rezultat", None)
            tk.Label(res, text=f"Scor: {fb.get('points', 0)}/100",
                     bg=c["card"], fg=c["text"], font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(0, 6))
            tk.Label(res, text=fb.get("message", ""), bg=c["card"], fg=c["text"],
                     wraplength=980, justify="left").pack(anchor="w", padx=14, pady=(0, 8))
            tk.Label(res, text=f"Răspuns corect: {fb.get('correct_answer', '')}",
                     bg=c["card"], fg=c["text"]).pack(anchor="w", padx=14, pady=(0, 12))

    def _csp_evaluate(self):
        items = self.state["csp"]["items"]
        idx = self.state["csp"]["idx"]
        if not items:
            return
        item = items[idx]
        checker = CSPAnswerChecker()
        user = self.csp_answer.get().strip()
        fb = checker.get_csp_feedback(item["answer"], user, item["explanation"])
        item["feedback"] = fb
        self._csp_render()

    def _csp_show_explanation(self):
        items = self.state["csp"]["items"]
        idx = self.state["csp"]["idx"]
        if not items:
            return
        item = items[idx]
        fb = item.get("feedback") or {"points": 0}
        messagebox.showinfo("Explicație", f"📊 Punctaj: {fb.get('points', 0)}/100\n\n🔍 Explicație:\n{item.get('explanation','')}")

    def _csp_prev(self):
        if self.state["csp"]["idx"] > 0:
            self.state["csp"]["idx"] -= 1
            self._csp_render()

    def _csp_next(self):
        items = self.state["csp"]["items"]
        if not items:
            return
        if self.state["csp"]["idx"] < len(items) - 1:
            self.state["csp"]["idx"] += 1
            self._csp_render()
        else:
            messagebox.showinfo("Gata", "Ai ajuns la finalul setului de întrebări CSP ✅")

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------
    def page_search(self, parent):
        c = self.colors[self.theme]
        self.page_title(parent, "Search — Generare & Evaluare", None)

        controls = self.card(parent, "Setări", "Generează un set de întrebări Search.")
        row = tk.Frame(controls, bg=c["card"])
        row.pack(fill="x", padx=14, pady=(0, 12))

        tk.Label(row, text="Număr întrebări:", bg=c["card"], fg=c["text"],
                 font=("Segoe UI", 11)).pack(side="left")

        self.search_count = tk.StringVar(value="3")
        tk.Entry(row, textvariable=self.search_count, width=6,
                 bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]).pack(side="left", padx=10)

        self.primary_button(row, "Generează", self._search_generate).pack(side="left", padx=10)

        self.search_area = tk.Frame(parent, bg=c["bg"])
        self.search_area.pack(fill="both", expand=True)

        self._search_render()

    def _search_generate(self):
        try:
            n = int(self.search_count.get())
            if n <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Atenție", "Introduce un număr valid (>0).")
            return

        qgen = SearchQuestion()
        items = []
        for _ in range(n):
            q_text, answer, explanation = qgen.generate()
            items.append({"q": q_text, "answer": answer, "explanation": explanation, "feedback": None})

        self.state["search"]["items"] = items
        self.state["search"]["idx"] = 0
        self._search_render()

    def _search_render(self):
        c = self.colors[self.theme]
        for w in self.search_area.winfo_children():
            w.destroy()

        items = self.state["search"]["items"]
        idx = self.state["search"]["idx"]
        if not items:
            card = self.card(self.search_area, "Întrebări", "Generează întrebări ca să începi.")
            tk.Label(card, text="Apasă „Generează” din setări.",
                     bg=c["card"], fg=c["muted"]).pack(anchor="w", padx=14, pady=(0, 12))
            return

        item = items[idx]
        qcard = self.card(self.search_area, f"Întrebarea {idx+1}/{len(items)}", None)
        tk.Label(qcard, text=item["q"], bg=c["card"], fg=c["text"],
                 wraplength=980, justify="left").pack(anchor="w", padx=14, pady=(0, 10))

        ans_card = self.card(self.search_area, "Răspuns", "Introdu răspunsul tău și apasă Evaluează.")
        self.search_answer = tk.StringVar()
        tk.Entry(ans_card, textvariable=self.search_answer, width=60,
                 bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]).pack(anchor="w", padx=14, pady=(0, 10))

        btn_row = tk.Frame(ans_card, bg=c["card"])
        btn_row.pack(fill="x", padx=14, pady=(0, 12))

        self.primary_button(btn_row, "✅ Evaluează", self._search_evaluate).pack(side="left")
        self.ghost_button(btn_row, "📘 Explicație", self._search_show_explanation).pack(side="left", padx=10)
        self.ghost_button(btn_row, "⬅️ Înapoi", self._search_prev).pack(side="right")
        self.ghost_button(btn_row, "➡️ Următoarea", self._search_next).pack(side="right", padx=10)

        if item.get("feedback"):
            fb = item["feedback"]
            res = self.card(self.search_area, "Rezultat", None)
            tk.Label(res, text=f"Scor: {fb.get('points', 0)}/100",
                     bg=c["card"], fg=c["text"], font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(0, 6))
            tk.Label(res, text=fb.get("message", ""), bg=c["card"], fg=c["text"],
                     wraplength=980, justify="left").pack(anchor="w", padx=14, pady=(0, 8))
            tk.Label(res, text=f"Răspuns corect: {fb.get('correct_answer', '')}",
                     bg=c["card"], fg=c["text"]).pack(anchor="w", padx=14, pady=(0, 12))

    def _search_evaluate(self):
        items = self.state["search"]["items"]
        idx = self.state["search"]["idx"]
        if not items:
            return
        item = items[idx]
        checker = SearchAnswerChecker()
        user = self.search_answer.get().strip()
        fb = checker.get_feedback(item["answer"], user, item["explanation"])
        item["feedback"] = fb
        self._search_render()

    def _search_show_explanation(self):
        items = self.state["search"]["items"]
        idx = self.state["search"]["idx"]
        if not items:
            return
        item = items[idx]
        fb = item.get("feedback") or {"points": 0}
        messagebox.showinfo("Explicație", f"📊 Punctaj: {fb.get('points', 0)}/100\n\n🔍 Explicație:\n{item.get('explanation','')}")

    def _search_prev(self):
        if self.state["search"]["idx"] > 0:
            self.state["search"]["idx"] -= 1
            self._search_render()

    def _search_next(self):
        items = self.state["search"]["items"]
        if not items:
            return
        if self.state["search"]["idx"] < len(items) - 1:
            self.state["search"]["idx"] += 1
            self._search_render()
        else:
            messagebox.showinfo("Gata", "Ai ajuns la finalul setului de întrebări Search ✅")

    # ------------------------------------------------------------------
    # USER QUERY: NASH
    # ------------------------------------------------------------------
    def page_ask_nash(self, parent):
        c = self.colors[self.theme]
        self.page_title(parent, "Pune o întrebare — Nash",
                        "Scrii întrebarea ta, apoi NashUserQuery o rezolvă.")

        info = self.card(parent, "Format acceptat", "Exemple (din Main.py):")
        examples = (
            "• aleatoriu, cate echilibre Nash pure?\n"
            "• [[(1,1) (2,2)] [(3,3) (2,1)]]; [A1, B1]; [A2, B2]; care sunt echilibrele Nash pure?\n"
        )
        tk.Label(info, text=examples, bg=c["card"], fg=c["text"],
                 justify="left", font=("Segoe UI", 11)).pack(anchor="w", padx=14, pady=(0, 12))

        inp = self.card(parent, "Întrebarea ta", None)
        self.ask_nash_input = scrolledtext.ScrolledText(
            inp, height=6, width=120,
            bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]
        )
        self.ask_nash_input.pack(fill="x", padx=14, pady=(0, 10))

        btn_row = tk.Frame(inp, bg=c["card"])
        btn_row.pack(fill="x", padx=14, pady=(0, 12))
        self.primary_button(btn_row, "Procesează", self._ask_nash_process).pack(side="left")
        self.ghost_button(btn_row, "Curăță", lambda: self.ask_nash_input.delete("1.0", "end")).pack(side="left", padx=10)

        out = self.card(parent, "Rezultat", None)
        self.ask_nash_output = scrolledtext.ScrolledText(
            out, height=14, width=120,
            bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]
        )
        self.ask_nash_output.pack(fill="both", padx=14, pady=(0, 12))

    def _ask_nash_process(self):
        text = self.ask_nash_input.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Atenție", "Scrie o întrebare Nash.")
            return

        engine = NashUserQuery()
        result = engine.process(text)

        self.ask_nash_output.delete("1.0", "end")
        if isinstance(result, str):
            self.ask_nash_output.insert("end", f"Eroare: {result}")
            return

        self.ask_nash_output.insert("end", "Jocul este:\n")
        for r in result.get("matrix", []):
            self.ask_nash_output.insert("end", f"{r}\n")
        self.ask_nash_output.insert("end", f"\nPlayer1 strategies: {result.get('player1')}\n")
        self.ask_nash_output.insert("end", f"Player2 strategies: {result.get('player2')}\n")
        self.ask_nash_output.insert("end", f"Tip întrebare: {result.get('question_type')}\n")
        self.ask_nash_output.insert("end", f"Răspuns: {result.get('answer')}\n")

    # ------------------------------------------------------------------
    # USER QUERY: MINMAX
    # ------------------------------------------------------------------
    def page_ask_minmax(self, parent):
        c = self.colors[self.theme]
        self.page_title(parent, "Pune o întrebare — MinMax",
                        "Scrii întrebarea ta, apoi MinMaxUserQuery o rezolvă.")

        info = self.card(parent, "Format acceptat", "Exemple (din Main.py):")
        examples = (
            "• aleatoriu\n"
            "• 3; 3,1,5,2; 2,2,2; Care va fi valoarea radacinii?\n"
        )
        tk.Label(info, text=examples, bg=c["card"], fg=c["text"],
                 justify="left", font=("Segoe UI", 11)).pack(anchor="w", padx=14, pady=(0, 12))

        inp = self.card(parent, "Întrebarea ta", None)
        self.ask_minmax_input = scrolledtext.ScrolledText(
            inp, height=6, width=120,
            bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]
        )
        self.ask_minmax_input.pack(fill="x", padx=14, pady=(0, 10))

        btn_row = tk.Frame(inp, bg=c["card"])
        btn_row.pack(fill="x", padx=14, pady=(0, 12))
        self.primary_button(btn_row, "Procesează", self._ask_minmax_process).pack(side="left")
        self.ghost_button(btn_row, "Curăță", lambda: self.ask_minmax_input.delete("1.0", "end")).pack(side="left", padx=10)

        out = self.card(parent, "Rezultat", None)
        self.ask_minmax_output = scrolledtext.ScrolledText(
            out, height=14, width=120,
            bg=c["input_bg"], fg=c["text"], insertbackground=c["text"]
        )
        self.ask_minmax_output.pack(fill="both", padx=14, pady=(0, 12))

    def _ask_minmax_process(self):
        text = self.ask_minmax_input.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Atenție", "Scrie o întrebare MinMax.")
            return

        engine = MinMaxUserQuery()
        result = engine.process(text)

        self.ask_minmax_output.delete("1.0", "end")
        if isinstance(result, str):
            self.ask_minmax_output.insert("end", f"Eroare: {result}")
            return

        self.ask_minmax_output.insert("end", "Detalii arbore MinMax:\n")
        self.ask_minmax_output.insert("end", f"Adâncime: {result.get('depth')}\n")
        self.ask_minmax_output.insert("end", f"Valori frunze: {result.get('leaf_values')}\n")
        if "structure" in result:
            self.ask_minmax_output.insert("end", f"Structură: {result.get('structure')}\n")
        self.ask_minmax_output.insert("end", f"\nÎntrebare: {result.get('question')}\n")
        self.ask_minmax_output.insert("end", f"Răspuns: {result.get('answer')}\n")


if __name__ == "__main__":
    app = AIExamUI()
    app.mainloop()
