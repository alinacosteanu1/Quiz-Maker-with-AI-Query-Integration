import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import json
import random
import requests
from backend import load_quizuri, save_quizuri, adauga_in_leaderboard, citeste_leaderboard

# ==== Configurare ====
QUESTION_TIME = 30
PROGRESS_STYLE = "green.Horizontal.TProgressbar"

# ==== Încarcă cheia API ====
config_path = os.path.join(os.path.dirname(__file__), "config.json")
try:
    with open(config_path, "r") as f:
        config = json.load(f)
    DEEPSEEK_API_KEY = config.get("deepseek_api_key", "")
except:
    DEEPSEEK_API_KEY = ""
    print("Config.json nu a fost găsit. API-ul nu va funcționa.")


# Formatare Aspect Interfata- Buton Rotunjit
class RoundedButton(tk.Canvas):
    def __init__(self, master, text="", command=None, radius=12, padding=(14, 8),
                 bg="#4B8BBE", fg="white", font=("Arial", 12, "bold"), hover="#3a6f9a", **kw):
        width = kw.pop('width', 200)
        height = padding[1] * 2 + 20

        super().__init__(master, width=width, height=height,
                         highlightthickness=0, bg=master["bg"], **kw)

        self.command = command
        self.bg = bg
        self.fg = fg
        self.hover_color = hover
        self.radius = radius
        self.font = font
        self.padding = padding
        self.text = text
        self._is_hover = False

        self._draw_button()
        self.bind("<Button-1>", lambda e: self._on_click())
        self.bind("<Enter>", lambda e: self._on_enter())
        self.bind("<Leave>", lambda e: self._on_leave())

    def _draw_button(self):
        self.delete("all")
        w = int(self["width"])
        h = int(self["height"])
        r = self.radius
        color = self.hover_color if self._is_hover else self.bg

        # Colțuri rotunjite
        self.create_arc((0, 0, 2 * r, 2 * r), start=90, extent=90, fill=color, outline=color)
        self.create_arc((w - 2 * r, 0, w, 2 * r), start=0, extent=90, fill=color, outline=color)
        self.create_arc((0, h - 2 * r, 2 * r, h), start=180, extent=90, fill=color, outline=color)
        self.create_arc((w - 2 * r, h - 2 * r, w, h), start=270, extent=90, fill=color, outline=color)

        # Părți drepte
        self.create_rectangle((r, 0, w - r, h), fill=color, outline=color)
        self.create_rectangle((0, r, w, h - r), fill=color, outline=color)

        # Text
        self.create_text(w // 2, h // 2, text=self.text, font=self.font,
                         fill=self.fg, tags="text")

    def _on_click(self):
        if callable(self.command):
            self.command()

    def _on_enter(self):
        self._is_hover = True
        self._draw_button()

    def _on_leave(self):
        self._is_hover = False
        self._draw_button()

    def configure_text(self, text):
        self.text = text
        self._draw_button()

    def configure(self, **kwargs):
        """Override configure method to handle custom options"""
        if 'bg' in kwargs:
            self.bg = kwargs['bg']
        if 'hover' in kwargs:
            self.hover_color = kwargs['hover']
        if 'text' in kwargs:
            self.text = kwargs['text']
        self._draw_button()


# ==== Aplicația Principală ====
class QuizApp:
    # Culori pentru categorii
    teme_categorii = {
        "biologie marina": {"bg": "#E0F7FF", "text": "#003366", "btn": "#2E8BC0"},
        "filme": {"bg": "#FFF5DB", "text": "#000000", "btn": "#FF6B35"},
        "cultura generala": {"bg": "#FFF0E0", "text": "#222222", "btn": "#FF9F1C"},
        "folclor romanesc": {"bg": "#FFF0F0", "text": "#6B0000", "btn": "#C44536"},
        "astronomie": {"bg": "#0b1b2b", "text": "#ffffff", "btn": "#6D597A"},
        "gastronomie": {"bg": "#FFF8E1", "text": "#5e3a00", "btn": "#E76F51"},
        "stiinta": {"bg": "#F3F0FF", "text": "#2e0854", "btn": "#6A4C93"}
    }

    def __init__(self, master):
        self.master = master
        master.title("🎯 Quiz Game AI")
        master.geometry("800x600")
        master.configure(bg="#f0f2f5")
        master.resizable(False, False)

        # Variabile de stare
        self.nume = ""
        self.intrebari = []
        self.index = 0
        self.scor = 0
        self.categorie_curenta = ""
        self.time_left = QUESTION_TIME
        self.timer_job = None

        # Încarcă quizurile existente
        self.quizuri = load_quizuri()

        # Stiluri
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(PROGRESS_STYLE, troughcolor="#e1e4ea",
                        background="#6ac1a0", thickness=20)

        # Crează interfața
        self.creaza_interfata_start()

    def creaza_interfata_start(self):
        """Creează ecranul de start"""
        # Frame principal
        self.frame_start = tk.Frame(self.master, bg=self.master["bg"])
        self.frame_start.place(relx=0.5, rely=0.5, anchor="center")

        # Titlu
        tk.Label(self.frame_start, text="🎯 Quiz Game AI",
                 font=("Arial", 28, "bold"), bg=self.master["bg"],
                 fg="#2c3e50").pack(pady=(0, 10))

        tk.Label(self.frame_start, text="Testează-ți cunoștințele!",
                 font=("Arial", 14), bg=self.master["bg"], fg="#7f8c8d").pack(pady=(0, 20))

        # Nume
        tk.Label(self.frame_start, text="Introduceți numele:",
                 font=("Arial", 12, "bold"), bg=self.master["bg"]).pack()

        self.entry_nume = tk.Entry(self.frame_start, font=("Arial", 14),
                                   width=30, relief="flat", bg="white")
        self.entry_nume.pack(pady=10, ipady=8)
        self.entry_nume.insert(0, "Jucător")
        self.entry_nume.bind("<FocusIn>", lambda e: self.entry_nume.select_range(0, tk.END))

        # Butoane principale
        btn_frame = tk.Frame(self.frame_start, bg=self.master["bg"])
        btn_frame.pack(pady=20)

        self.btn_categorii = RoundedButton(btn_frame, text="📚 Categorii existente",
                                           command=self.alege_categorie,
                                           bg="#3498db", hover="#2980b9",
                                           width=250)
        self.btn_categorii.pack(side="left", padx=10)

        self.btn_ai = RoundedButton(btn_frame, text="🤖 Generează quiz AI",
                                    command=self.genereaza_quiz_ai,
                                    bg="#9b59b6", hover="#8e44ad",
                                    width=250)
        self.btn_ai.pack(side="left", padx=10)

        # Leaderboard
        tk.Label(self.frame_start, text="🏆 Top Scoruri",
                 font=("Arial", 13, "bold"), bg=self.master["bg"]).pack(pady=(30, 5))

        frame_lb = tk.Frame(self.frame_start, bg="white", relief="solid",
                            borderwidth=1, width=400, height=150)
        frame_lb.pack(pady=(0, 10))
        frame_lb.pack_propagate(False)

        self.lb_text = tk.Text(frame_lb, width=48, height=8,
                               state="disabled", font=("Arial", 10),
                               bg="white", relief="flat")
        self.lb_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.actualizeaza_leaderboard()

    def actualizeaza_leaderboard(self):
        """Actualizează afișajul leaderboard"""
        self.lb_text.config(state="normal")
        self.lb_text.delete(1.0, tk.END)

        leaderboard = citeste_leaderboard()
        if not leaderboard or leaderboard == "Niciun scor înregistrat încă.\nFii primul!":
            self.lb_text.insert(tk.END, leaderboard)
        else:
            lines = leaderboard.strip().split('\n')
            for line in lines:
                self.lb_text.insert(tk.END, line + '\n')

        self.lb_text.config(state="disabled")

    def alege_categorie(self):
        """Deschide fereastra de alegere categorie"""
        self.nume = self.entry_nume.get().strip()
        if not self.nume or self.nume == "Jucător":
            self.nume = "Jucător"

        # Fereastra pentru categorii
        self.win_cat = tk.Toplevel(self.master)
        self.win_cat.title("📂 Alege categoria")
        self.win_cat.geometry("500x500")
        self.win_cat.configure(bg="#f0f2f5")
        self.win_cat.resizable(False, False)
        self.win_cat.grab_set()

        # Titlu
        tk.Label(self.win_cat, text=f"👋 Salut, {self.nume}!",
                 font=("Arial", 16, "bold"), bg="#f0f2f5").pack(pady=15)

        tk.Label(self.win_cat, text="Alege o categorie:",
                 font=("Arial", 12), bg="#f0f2f5").pack()

        # Frame pentru butoane cu scroll
        container = tk.Frame(self.win_cat, bg="#f0f2f5")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg="#f0f2f5", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#f0f2f5")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Sortează categoriile
        categorii = list(self.quizuri.keys())
        categorii.sort()

        # Butoane pentru fiecare categorie
        for cat in categorii:
            # Determină culoarea butonului
            tema = self.teme_categorii.get(cat, {"btn": "#4B8BBE"})
            btn_color = tema["btn"]

            btn = RoundedButton(scroll_frame, text=cat.title(),
                                command=lambda c=cat: self.start_quiz(c),
                                bg=btn_color, hover="#34495e",
                                width=350)
            btn.pack(pady=6, padx=20, fill="x")

        # Buton pentru creare categorie nouă
        btn_nou = RoundedButton(scroll_frame, text="➕ Creează categorie nouă",
                                command=self.creaza_categorie_noua,
                                bg="#2ecc71", hover="#27ae60",
                                width=350)
        btn_nou.pack(pady=15, padx=20, fill="x")

        # Afișează scrollbar doar dacă este necesar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def creaza_categorie_noua(self):
        """Creează o categorie nouă"""
        domeniu = simpledialog.askstring("Categorie nouă",
                                         "Introdu numele noii categorii:")
        if not domeniu:
            return

        domeniu = domeniu.strip().lower()
        if domeniu in self.quizuri:
            messagebox.showinfo("Există deja",
                                f"Categoria '{domeniu}' există deja!")
            return

        # Adaugă categoria goală
        self.quizuri[domeniu] = []
        save_quizuri(self.quizuri)

        messagebox.showinfo("Succes",
                            f"Categoria '{domeniu}' a fost creată!\n"
                            f"Acum poți genera quiz-uri pentru ea.")

        # Închide și redeschide fereastra
        self.win_cat.destroy()
        self.alege_categorie()

    def start_quiz(self, categorie):
        """Începe quiz-ul pentru categoria selectată - VERSIUNE CORECTĂ"""
        try:
            self.win_cat.destroy()
        except:
            pass

        self.categorie_curenta = categorie
        questions = self.quizuri.get(categorie, [])

        if not questions:
            messagebox.showwarning("Categorie goală",
                                   f"Categoria '{categorie}' nu are întrebări.")
            return

        # Asigură-te că avem suficiente întrebări
        if len(questions) < 5:
            # Dacă sunt prea puține întrebări, folosește-le pe toate
            self.intrebari = questions.copy()
        else:
            # Altfel alege maxim 10 întrebări aleatoriu
            num_to_select = min(10, len(questions))
            self.intrebari  = random.sample(questions, k=num_to_select)

        print(f"✅ Întrebări selectate: {len(self.intrebari)}")  # Confirmare

        self.index = 0
        self.scor = 0
        self.time_left = QUESTION_TIME

        # Ascunde ecranul de start
        self.frame_start.place_forget()

        # Creează interfața quiz
        self.creaza_interfata_quiz()

    def genereaza_intrebari_ai_pentru_categorie(self, categorie):
        """Generează întrebări AI pentru o categorie existentă"""
        if not DEEPSEEK_API_KEY:
            messagebox.showerror("Eroare",
                                 "Nu este configurată cheia API.\n"
                                 "Completează config.json sau folosește quiz-uri existente.")
            return

        # Generează întrebări
        intrebari = self.genereaza_intrebari_deepseek(categorie)
        if intrebari:
            # Salvează întrebările
            self.quizuri[categorie] = intrebari
            save_quizuri(self.quizuri)

            # Pornește quiz-ul
            self.intrebari = intrebari
            self.index = 0
            self.scor = 0
            self.time_left = QUESTION_TIME
            self.frame_start.place_forget()
            self.creaza_interfata_quiz()
        else:
            messagebox.showerror("Eroare", "Nu s-au putut genera întrebări.")

    def creaza_interfata_quiz(self):
        """Creează interfața pentru quiz"""
        # Determină tema
        tema = self.teme_categorii.get(self.categorie_curenta,
                                       {"bg": "#ffffff", "text": "#000000", "btn": "#4B8BBE"})
        bg_color = tema["bg"]
        text_color = tema["text"]
        btn_color = tema["btn"]

        # Frame principal quiz
        self.frame_quiz = tk.Frame(self.master, bg=bg_color)
        self.frame_quiz.place(relx=0.5, rely=0.5, anchor="center",
                              width=750, height=550)

        # Antet
        header_frame = tk.Frame(self.frame_quiz, bg=bg_color)
        header_frame.pack(fill="x", pady=(20, 10), padx=20)

        tk.Label(header_frame, text=f"📝 {self.categorie_curenta.title()}",
                 font=("Arial", 20, "bold"), bg=bg_color, fg=text_color).pack(side="left")

        tk.Label(header_frame, text=f"👤 {self.nume}",
                 font=("Arial", 12), bg=bg_color, fg=text_color).pack(side="right")

        # Scor și progres
        info_frame = tk.Frame(self.frame_quiz, bg=bg_color)
        info_frame.pack(fill="x", pady=(0, 20), padx=20)

        self.lbl_scor = tk.Label(info_frame,
                                 text=f"Scor: {self.scor} | Întrebarea: {self.index + 1}/{len(self.intrebari)}",
                                 font=("Arial", 12, "bold"), bg=bg_color, fg=text_color)
        self.lbl_scor.pack(side="left")

        self.lbl_timer = tk.Label(info_frame,
                                  text=f"⏰ Timp: {self.time_left}s",
                                  font=("Arial", 12, "bold"), bg=bg_color, fg=text_color)
        self.lbl_timer.pack(side="right")

        # Întrebare
        question_frame = tk.Frame(self.frame_quiz, bg=bg_color,
                                  relief="solid", borderwidth=2)
        question_frame.pack(fill="x", padx=40, pady=(0, 30))

        self.label_intrebare = tk.Label(question_frame, text="",
                                        font=("Arial", 16, "bold"),
                                        wraplength=600, justify="center",
                                        bg="#ffffff", fg="#000000",
                                        padx=20, pady=20)
        self.label_intrebare.pack(fill="both", expand=True)

        # Butoane pentru răspunsuri
        self.choice_buttons = []
        for i in range(4):
            btn = RoundedButton(self.frame_quiz, text="",
                                command=lambda idx=i: self.on_choice(idx),
                                bg=btn_color, hover="#2c3e50",
                                width=500)
            btn.pack(pady=8)
            self.choice_buttons.append(btn)

        # Feedback
        self.lbl_feedback = tk.Label(self.frame_quiz, text="",
                                     font=("Arial", 12, "italic"),
                                     bg=bg_color, fg=text_color)
        self.lbl_feedback.pack(pady=(20, 0))

        # Buton pentru următoarea întrebare
        self.btn_urmator = RoundedButton(self.frame_quiz, text="Următoarea →",
                                         command=self.next_question,
                                         bg="#2ecc71", hover="#27ae60",
                                         width=200)
        self.btn_urmator.pack(pady=10)
        self.btn_urmator.place_forget()  # Ascuns inițial

        # Afișează prima întrebare
        self.afiseaza_intrebarea()

    def afiseaza_intrebarea(self):
        """Afișează întrebarea curentă"""
        if self.index >= len(self.intrebari):
            self.finalize_quiz()
            return

        q = self.intrebari[self.index]

        # Actualizează întrebarea
        self.label_intrebare.config(text=q["intrebare"])

        # Actualizează butoanele
        vars_order = ["a", "b", "c", "d"]
        for btn, lit in zip(self.choice_buttons, vars_order):
            text = q["variante"].get(lit, "")
            btn.configure_text(f"{lit.upper()}) {text}")
            # Re-atașează event handler
            btn.bind("<Button-1>", lambda e, idx=self.choice_buttons.index(btn): self.on_choice(idx))

        # Actualizează informații
        self.lbl_scor.config(text=f"Scor: {self.scor} | Întrebarea: {self.index + 1}/{len(self.intrebari)}")

        # Ascunde feedback și butonul următor
        self.lbl_feedback.config(text="")
        self.btn_urmator.place_forget()

        # Resetează timer-ul
        if self.timer_job:
            self.master.after_cancel(self.timer_job)
        self.time_left = QUESTION_TIME
        self.lbl_timer.config(text=f"⏰ Timp: {self.time_left}s")
        self.start_timer()

    def start_timer(self):
        """Pornește timer-ul pentru întrebare"""
        if self.time_left > 0:
            self.time_left -= 1
            self.lbl_timer.config(text=f"⏰ Timp: {self.time_left}s")
            self.timer_job = self.master.after(1000, self.start_timer)
        else:
            # Timp expirat - treci la următoarea întrebare
            self.lbl_feedback.config(text="⏰ Timp expirat!", fg="#e74c3c")
            self.master.after(1500, self.next_question)

    def on_choice(self, idx):
        """Gestionează selecția unui răspuns"""
        # Oprește timer-ul
        if self.timer_job:
            self.master.after_cancel(self.timer_job)
            self.timer_job = None

        lit = ["a", "b", "c", "d"][idx]
        q = self.intrebari[self.index]

        # Dezactivează toate butoanele (elimină bindings)
        for btn in self.choice_buttons:
            btn.unbind("<Button-1>")

        # Verifică răspunsul
        if lit == q["corect"]:
            self.scor += 1
            self.lbl_feedback.config(text="✅ Corect!", fg="#27ae60")
            # Highlight butonul corect
            self.choice_buttons[idx].configure(bg="#27ae60", hover="#27ae60")
        else:
            self.lbl_feedback.config(text=f"❌ Greșit! Răspunsul corect era: {q['corect'].upper()}",
                                     fg="#e74c3c")
            # Highlight butonul greșit cu roșu și corectul cu verde
            self.choice_buttons[idx].configure(bg="#e74c3c", hover="#e74c3c")
            # Găsește butonul corect
            correct_idx = ["a", "b", "c", "d"].index(q["corect"])
            self.choice_buttons[correct_idx].configure(bg="#27ae60", hover="#27ae60")

        # Afișează butonul pentru următoarea întrebare
        self.btn_urmator.place(relx=0.5, rely=0.95, anchor="s")

    def next_question(self):
        """Trece la următoarea întrebare"""
        self.index += 1
        if self.index >= len(self.intrebari):
            self.finalize_quiz()
        else:
            # Resetează culorile butoanelor
            tema = self.teme_categorii.get(self.categorie_curenta, {"btn": "#4B8BBE"})
            btn_color = tema["btn"]
            for btn in self.choice_buttons:
                btn.configure(bg=btn_color, hover="#2c3e50")

            self.afiseaza_intrebarea()

    def finalize_quiz(self):
        """Finalizează quiz-ul și afișează rezultatul"""
        # Salvează scorul
        adauga_in_leaderboard(self.nume, self.scor, len(self.intrebari))

        # Afișează rezultatul
        procent = (self.scor / len(self.intrebari)) * 100

        if procent >= 80:
            mesaj = f"🎉 EXCELENT! {self.nume}\n\n"
            culoare = "#27ae60"
        elif procent >= 60:
            mesaj = f"👍 BINE! {self.nume}\n\n"
            culoare = "#f39c12"
        else:
            mesaj = f"💪 AI FĂCUT-O! {self.nume}\n\n"
            culoare = "#e74c3c"

        mesaj += f"Scor final: {self.scor}/{len(self.intrebari)}\n"
        mesaj += f"Procentaj: {procent:.1f}%\n\n"
        mesaj += f"Categorie: {self.categorie_curenta.title()}"

        # Ascunde interfața quiz
        self.frame_quiz.destroy()

        # Afișează ecranul de rezultat
        self.frame_result = tk.Frame(self.master, bg="#f0f2f5")
        self.frame_result.place(relx=0.5, rely=0.5, anchor="center",
                                width=400, height=300)

        tk.Label(self.frame_result, text="🏁 REZULTAT",
                 font=("Arial", 24, "bold"), bg="#f0f2f5").pack(pady=20)

        tk.Label(self.frame_result, text=mesaj,
                 font=("Arial", 14), bg="#f0f2f5", fg=culoare,
                 justify="center").pack(pady=20)

        # Butoane pentru acțiuni
        btn_frame = tk.Frame(self.frame_result, bg="#f0f2f5")
        btn_frame.pack(pady=20)

        RoundedButton(btn_frame, text="🔄 Joacă din nou",
                      command=self.restart_quiz,
                      bg="#3498db", hover="#2980b9").pack(side="left", padx=5)

        RoundedButton(btn_frame, text="🏠 Meniul principal",
                      command=self.back_to_menu,
                      bg="#9b59b6", hover="#8e44ad").pack(side="left", padx=5)

        RoundedButton(btn_frame, text="📊 Leaderboard",
                      command=self.vezi_leaderboard,
                      bg="#2ecc71", hover="#27ae60").pack(side="left", padx=5)

    def restart_quiz(self):
        """Reîncepe quiz-ul curent"""
        self.frame_result.destroy()
        self.frame_quiz.destroy()
        self.intrebari = random.sample(self.quizuri[self.categorie_curenta],
                                       k=min(10, len(self.quizuri[self.categorie_curenta])))
        self.index = 0
        self.scor = 0
        self.time_left = QUESTION_TIME
        self.creaza_interfata_quiz()

    def back_to_menu(self):
        """Întoarce la meniul principal"""
        self.frame_result.destroy()
        self.frame_quiz.destroy()
        self.frame_start.place(relx=0.5, rely=0.5, anchor="center")
        self.actualizeaza_leaderboard()

    def vezi_leaderboard(self):
        """Afișează leaderboard complet"""
        leaderboard = citeste_leaderboard()

        win_lb = tk.Toplevel(self.master)
        win_lb.title("🏆 Leaderboard Complet")
        win_lb.geometry("400x500")
        win_lb.configure(bg="#f0f2f5")
        win_lb.resizable(False, False)

        tk.Label(win_lb, text="🏆 TOP SCORURI",
                 font=("Arial", 20, "bold"), bg="#f0f2f5").pack(pady=20)

        text_widget = tk.Text(win_lb, width=45, height=20,
                              font=("Arial", 11), bg="white", relief="flat")
        text_widget.pack(padx=20, pady=10)

        text_widget.insert(tk.END, leaderboard)
        text_widget.config(state="disabled")

    def genereaza_quiz_ai(self):
        """Generează un quiz nou folosind AI"""
        self.nume = self.entry_nume.get().strip()
        if not self.nume or self.nume == "Jucător":
            self.nume = "Jucător"

        if not DEEPSEEK_API_KEY:
            messagebox.showerror("Eroare",
                                 "Cheia API nu este configurată!\n\n"
                                 "1. Obține o cheie gratuită de la https://platform.deepseek.com/\n"
                                 "2. Adaugă cheia în config.json\n\n"
                                 "Pentru testare, folosește categoriile existente.")
            return

        domeniu = simpledialog.askstring("🤖 Generează quiz AI",
                                         "Introdu un subiect pentru noul quiz:\n\n"
                                         "Exemple: istorie, sport, muzică, tehnologie...")

        if not domeniu:
            return

        domeniu = domeniu.strip().lower()

        # Generează întrebări
        intrebari = self.genereaza_intrebari_deepseek(domeniu)

        if not intrebari:
            messagebox.showerror("Eroare", "Nu s-au putut genera întrebări.")
            return

        # Salvează quiz-ul nou
        self.quizuri[domeniu] = intrebari
        save_quizuri(self.quizuri)

        # Pornește quiz-ul
        self.categorie_curenta = domeniu
        self.intrebari = intrebari
        self.index = 0
        self.scor = 0
        self.time_left = QUESTION_TIME

        self.frame_start.place_forget()
        self.creaza_interfata_quiz()

    def genereaza_intrebari_deepseek(self, domeniu):
        """Generează întrebări folosind DeepSeek API"""
        if not DEEPSEEK_API_KEY:
            return self.genereaza_intrebari_mock(domeniu)

        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"""Generează 10 întrebări de quiz pe tema: {domeniu}

        Cerințe:
        1. Fiecare întrebare să fie clară și concisă
        2. 4 opțiuni de răspuns pentru fiecare întrebare (a, b, c, d)
        3. Indică litera răspunsului corect
        4. Formatează răspunsul EXACT în JSON:

        {{
            "questions": [
                {{
                    "question": "text întrebare",
                    "options": {{
                        "a": "opțiune a",
                        "b": "opțiune b",
                        "c": "opțiune c", 
                        "d": "opțiune d"
                    }},
                    "correct": "a"
                }}
            ]
        }}

        IMPORTANT: Returnează DOAR JSON, fără text suplimentar."""

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Ești un expert în crearea de quiz-uri educaționale."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"]

            # Extrage JSON din răspuns
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)

            if json_match:
                json_str = json_match.group()
                quiz_data = json.loads(json_str)

                intrebari = []
                for q in quiz_data.get("questions", []):
                    intrebari.append({
                        "intrebare": q.get("question", ""),
                        "variante": q.get("options", {}),
                        "corect": q.get("correct", "a")
                    })

                return intrebari

            return self.genereaza_intrebari_mock(domeniu)

        except Exception as e:
            print(f"Eroare API: {e}")
            # Folosește mock data dacă API-ul eșuează
            return self.genereaza_intrebari_mock(domeniu)

    def genereaza_intrebari_mock(self, domeniu):
        """Generează întrebări mock pentru testare"""
        intrebari_mock = [
            {
                "intrebare": f"Ce înseamnă termenul '{domeniu}'?",
                "variante": {
                    "a": "Studiul fenomenelor naturale",
                    "b": "O disciplină academică",
                    "c": "O practică culturală",
                    "d": "Toate de mai sus"
                },
                "corect": "d"
            },
            {
                "intrebare": f"Când a apărut domeniul '{domeniu}'?",
                "variante": {
                    "a": "În antichitate",
                    "b": "În evul mediu",
                    "c": "În epoca modernă",
                    "d": "Depinde de context"
                },
                "corect": "d"
            },
            {
                "intrebare": f"Cine este un reprezentant important al '{domeniu}'?",
                "variante": {
                    "a": "Un cercetător cunoscut",
                    "b": "Un artist celebru",
                    "c": "Un lider istoric",
                    "d": "Depinde de domeniu"
                },
                "corect": "d"
            },
            {
                "intrebare": f"Care este aplicația practică a '{domeniu}'?",
                "variante": {
                    "a": "În educație",
                    "b": "În tehnologie",
                    "c": "În artă",
                    "d": "În multe domenii"
                },
                "corect": "d"
            },
            {
                "intrebare": f"De ce este important '{domeniu}'?",
                "variante": {
                    "a": "Dezvoltă gândirea critică",
                    "b": "Îmbunătățește abilitățile practice",
                    "c": "Extinde orizonturile culturale",
                    "d": "Toate de mai sus"
                },
                "corect": "d"
            }
        ]

        # Adaugă domeniul specific în unele întrebări
        for i in range(len(intrebari_mock)):
            intrebari_mock[i]["intrebare"] = intrebari_mock[i]["intrebare"].replace("{domeniu}", domeniu)

        return intrebari_mock


# ==== Pornirea aplicației ====
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()