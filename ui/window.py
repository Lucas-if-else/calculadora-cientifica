"""
ui/window.py
Main application window – scientific calculator GUI built with Tkinter.
Completely separated from business logic (engine/).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

from engine.calculator import Calculator
from .theme import THEMES, Theme


# ── Layout constants ──────────────────────────────────────────────────────────
FONT_DISPLAY   = ("Courier New", 30, "bold")
FONT_EXPR      = ("Courier New", 13)
FONT_BTN       = ("Segoe UI", 12, "bold")
FONT_BTN_SM    = ("Segoe UI", 10, "bold")
FONT_HISTORY   = ("Courier New", 10)
FONT_LABEL     = ("Segoe UI", 9)

BTN_H = 2          # button height (rows)
BTN_W = 5          # button width (chars)
PAD   = 3          # padding between buttons

# ── Button layout definition ──────────────────────────────────────────────────
#   (label, column_span, category)
#   categories: num, op, fn, eq, mem, spec, const
BUTTON_ROWS = [
    # Row 0 – memory
    [("MC",   1, "mem"), ("MR",   1, "mem"), ("M+",   1, "mem"), ("M-",   1, "mem"),
     ("MS",   1, "mem"), ("ans",  1, "const")],
    # Row 1 – functions top
    [("sin",  1, "fn"),  ("cos",  1, "fn"),  ("tan",  1, "fn"),  ("log",  1, "fn"),
     ("ln",   1, "fn"),  ("√",    1, "fn")],
    # Row 2 – functions mid
    [("asin", 1, "fn"),  ("acos", 1, "fn"),  ("atan", 1, "fn"),  ("x²",   1, "fn"),
     ("x³",   1, "fn"),  ("xⁿ",   1, "fn")],
    # Row 3 – constants + misc
    [("π",    1, "const"),("e",   1, "const"),("(",   1, "op"),  (")",    1, "op"),
     ("AC",   1, "spec"),("C",    1, "spec")],
    # Row 4 – numbers + ops
    [("7",    1, "num"), ("8",    1, "num"),  ("9",    1, "num"), ("÷",    1, "op"),
     ("%",    1, "op"),  ("±",    1, "fn")],
    # Row 5
    [("4",    1, "num"), ("5",    1, "num"),  ("6",    1, "num"), ("×",    1, "op"),
     ("1/x",  1, "fn"),  ("fact", 1, "fn")],
    # Row 6
    [("1",    1, "num"), ("2",    1, "num"),  ("3",    1, "num"), ("−",    1, "op"),
     ("⌫",    1, "spec"), ("",   1, "blank")],
    # Row 7
    [("0",    2, "num"), (".",    1, "num"),  ("+",    1, "op"),  ("=",    2, "eq")],
]


class CalcButton(tk.Button):
    """A calculator button with hover animation."""

    def __init__(self, master, text, category, theme: Theme, command, **kwargs):
        bg = self._bg(category, theme)
        fg = theme.fg_btn_eq if category == "eq" else theme.fg_btn
        if category == "spec":
            fg = "#ff4466"
        elif category == "mem":
            fg = theme.accent2
        elif category == "const":
            fg = theme.accent

        font = FONT_BTN_SM if len(text) > 3 else FONT_BTN
        super().__init__(
            master, text=text, bg=bg, fg=fg,
            activebackground=self._hover(category, theme),
            activeforeground=fg,
            font=font,
            relief="flat", bd=0,
            cursor="hand2",
            command=command,
            **kwargs
        )
        self._bg_normal  = bg
        self._bg_hover   = self._hover(category, theme)
        self.bind("<Enter>", lambda e: self.config(bg=self._bg_hover))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg_normal))

    @staticmethod
    def _bg(cat, t):
        return {
            "num":   t.bg_btn,
            "op":    t.bg_btn_op,
            "fn":    t.bg_btn_fn,
            "eq":    t.bg_btn_eq,
            "mem":   t.bg_btn_mem,
            "spec":  t.bg_btn_spec,
            "const": t.bg_btn_fn,
            "blank": t.bg_main,
        }.get(cat, t.bg_btn)

    @staticmethod
    def _hover(cat, t):
        return {
            "num":   t.hover_btn,
            "op":    t.hover_op,
            "fn":    t.hover_btn,
            "eq":    t.hover_eq,
            "mem":   t.hover_btn,
            "spec":  "#440010",
            "const": t.hover_btn,
            "blank": t.bg_main,
        }.get(cat, t.hover_btn)


class SolverDialog(tk.Toplevel):
    """Popup dialog for linear/quadratic equation solver."""

    def __init__(self, master, theme: Theme, calc: Calculator):
        super().__init__(master)
        self.theme = theme
        self.calc  = calc
        self.title("Equation Solver")
        self.configure(bg=theme.bg_main)
        self.resizable(False, False)
        self._build()
        self.grab_set()

    def _build(self):
        t = self.theme
        pad = {"padx": 12, "pady": 6}

        tk.Label(self, text="Equation Solver", font=("Segoe UI", 13, "bold"),
                 bg=t.bg_main, fg=t.accent).pack(pady=(16, 4))

        # Linear
        lf1 = tk.LabelFrame(self, text="Linear:  ax + b = 0",
                             bg=t.bg_main, fg=t.fg_main, font=FONT_LABEL, padx=10, pady=8)
        lf1.pack(fill="x", padx=16, pady=6)
        fr1 = tk.Frame(lf1, bg=t.bg_main); fr1.pack()
        self.la = self._entry(fr1, "a")
        self.lb = self._entry(fr1, "b")
        tk.Button(lf1, text="Solve Linear", bg=t.bg_btn_eq, fg=t.fg_btn_eq,
                  font=FONT_BTN_SM, relief="flat", cursor="hand2",
                  command=self._solve_linear).pack(pady=4)
        self.res_l = tk.Label(lf1, text="", bg=t.bg_main, fg=t.accent, font=FONT_EXPR)
        self.res_l.pack()

        # Quadratic
        lf2 = tk.LabelFrame(self, text="Quadratic:  ax² + bx + c = 0",
                             bg=t.bg_main, fg=t.fg_main, font=FONT_LABEL, padx=10, pady=8)
        lf2.pack(fill="x", padx=16, pady=6)
        fr2 = tk.Frame(lf2, bg=t.bg_main); fr2.pack()
        self.qa = self._entry(fr2, "a")
        self.qb = self._entry(fr2, "b")
        self.qc = self._entry(fr2, "c")
        tk.Button(lf2, text="Solve Quadratic", bg=t.bg_btn_eq, fg=t.fg_btn_eq,
                  font=FONT_BTN_SM, relief="flat", cursor="hand2",
                  command=self._solve_quad).pack(pady=4)
        self.res_q = tk.Label(lf2, text="", bg=t.bg_main, fg=t.accent, font=FONT_EXPR,
                               wraplength=320)
        self.res_q.pack()

        tk.Button(self, text="Close", bg=t.bg_btn_spec, fg="#ff4466",
                  relief="flat", cursor="hand2", font=FONT_BTN_SM,
                  command=self.destroy).pack(pady=(8, 16))

    def _entry(self, parent, label):
        t = self.theme
        tk.Label(parent, text=label + "=", bg=t.bg_main, fg=t.fg_main,
                 font=FONT_LABEL).pack(side="left", padx=4)
        e = tk.Entry(parent, width=7, bg=t.bg_display, fg=t.fg_display,
                     insertbackground=t.accent, font=FONT_EXPR, relief="flat")
        e.pack(side="left", padx=4)
        return e

    def _get_float(self, entry, name):
        try:
            return float(entry.get() or "0")
        except ValueError:
            raise ValueError(f"'{name}' must be a number")

    def _solve_linear(self):
        try:
            a = self._get_float(self.la, "a")
            b = self._get_float(self.lb, "b")
            self.res_l.config(text=self.calc.solve_linear(a, b))
        except ValueError as exc:
            self.res_l.config(text=f"Error: {exc}")

    def _solve_quad(self):
        try:
            a = self._get_float(self.qa, "a")
            b = self._get_float(self.qb, "b")
            c = self._get_float(self.qc, "c")
            self.res_q.config(text=self.calc.solve_quadratic(a, b, c))
        except ValueError as exc:
            self.res_q.config(text=f"Error: {exc}")


class MainWindow:
    """
    Primary application window.
    Owns the Tk root, all widgets, and delegates logic to Calculator.
    """

    def __init__(self):
        self.calc         = Calculator()
        self.theme        = THEMES["Cyberpunk"]
        self.expression   = ""        # current expression string
        self.just_solved  = False     # flag: result just calculated

        self.root = tk.Tk()
        self.root.title("Scientific Calculator")
        self.root.resizable(True, True)
        self.root.minsize(700, 560)

        self._build_ui()
        self._bind_keyboard()
        self._refresh_history()
        self.root.mainloop()

    # ── UI construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        t = self.theme
        self.root.configure(bg=t.bg_main)

        # ── Top toolbar ────────────────────────────────────────────────────
        toolbar = tk.Frame(self.root, bg=t.bg_main)
        toolbar.pack(fill="x", padx=10, pady=(8, 0))

        tk.Label(toolbar, text="⬡ CALC", font=("Courier New", 11, "bold"),
                 bg=t.bg_main, fg=t.accent).pack(side="left")

        # Theme selector
        tk.Label(toolbar, text="Theme:", bg=t.bg_main, fg=t.fg_main,
                 font=FONT_LABEL).pack(side="right", padx=(0, 4))
        self.theme_var = tk.StringVar(value=self.theme.name)
        tm = ttk.Combobox(toolbar, textvariable=self.theme_var,
                          values=list(THEMES.keys()), width=13, state="readonly")
        tm.pack(side="right", padx=4)
        tm.bind("<<ComboboxSelected>>", self._on_theme_change)

        # Solver button
        tk.Button(toolbar, text="∫ Solver", bg=t.bg_btn_fn, fg=t.accent,
                  font=FONT_BTN_SM, relief="flat", cursor="hand2",
                  command=self._open_solver).pack(side="right", padx=8)

        # ── Main body ──────────────────────────────────────────────────────
        body = tk.Frame(self.root, bg=t.bg_main)
        body.pack(fill="both", expand=True, padx=10, pady=8)

        # Left: display + buttons
        left = tk.Frame(body, bg=t.bg_main)
        left.pack(side="left", fill="both", expand=True)

        # Right: history sidebar
        right = tk.Frame(body, bg=t.bg_sidebar, width=190)
        right.pack(side="right", fill="y", padx=(8, 0))
        right.pack_propagate(False)
        self._build_sidebar(right)

        self._build_display(left)
        self._build_buttons(left)

    def _build_display(self, parent):
        t = self.theme
        disp = tk.Frame(parent, bg=t.bg_display, bd=0)
        disp.pack(fill="x", pady=(0, 6))

        # Memory indicator
        self.mem_label = tk.Label(disp, text="", font=FONT_LABEL,
                                   bg=t.bg_display, fg=t.accent2)
        self.mem_label.pack(anchor="e", padx=10, pady=(6, 0))

        # Expression preview (what user is typing)
        self.expr_var = tk.StringVar(value="")
        tk.Label(disp, textvariable=self.expr_var, font=FONT_EXPR,
                 bg=t.bg_display, fg=t.fg_expr,
                 anchor="e", justify="right").pack(fill="x", padx=12)

        # Main result display
        self.display_var = tk.StringVar(value="0")
        tk.Label(disp, textvariable=self.display_var, font=FONT_DISPLAY,
                 bg=t.bg_display, fg=t.fg_display,
                 anchor="e", justify="right").pack(fill="x", padx=12, pady=(2, 10))

        # Copy button
        copy_btn = tk.Button(disp, text="⎘ copy", font=FONT_LABEL,
                              bg=t.bg_display, fg=t.fg_history,
                              relief="flat", cursor="hand2",
                              command=self._copy_result)
        copy_btn.pack(anchor="e", padx=10, pady=(0, 6))

    def _build_buttons(self, parent):
        grid = tk.Frame(parent, bg=self.theme.bg_main)
        grid.pack(fill="both", expand=True)

        for r, row_def in enumerate(BUTTON_ROWS):
            col = 0
            for (text, span, cat) in row_def:
                if cat == "blank":
                    col += span
                    continue
                btn = CalcButton(
                    grid, text=text, category=cat, theme=self.theme,
                    command=lambda t=text: self._on_button(t),
                    width=BTN_W * span + (span - 1),
                    height=BTN_H,
                )
                btn.grid(row=r, column=col, columnspan=span,
                         padx=PAD, pady=PAD, sticky="nsew")
                col += span

        # Make all columns/rows expand equally
        cols = max(sum(span for _, span, _ in row) for row in BUTTON_ROWS)
        for c in range(cols):
            grid.columnconfigure(c, weight=1)
        for r in range(len(BUTTON_ROWS)):
            grid.rowconfigure(r, weight=1)

    def _build_sidebar(self, parent):
        t = self.theme
        tk.Label(parent, text="History", font=("Segoe UI", 10, "bold"),
                 bg=t.bg_sidebar, fg=t.accent).pack(pady=(10, 4))

        # Scrollable history list
        frame = tk.Frame(parent, bg=t.bg_sidebar)
        frame.pack(fill="both", expand=True, padx=4)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.history_list = tk.Listbox(
            frame, font=FONT_HISTORY,
            bg=t.bg_sidebar, fg=t.fg_history,
            selectbackground=t.bg_btn, selectforeground=t.accent,
            relief="flat", bd=0, highlightthickness=0,
            yscrollcommand=scrollbar.set,
            activestyle="none",
        )
        self.history_list.pack(fill="both", expand=True)
        scrollbar.config(command=self.history_list.yview)
        self.history_list.bind("<Double-Button-1>", self._on_history_click)

        # Clear history button
        tk.Button(parent, text="Clear History", bg=t.bg_btn_spec, fg="#ff4466",
                  font=FONT_LABEL, relief="flat", cursor="hand2",
                  command=self._clear_history).pack(pady=6)

    # ── Button / keyboard handlers ────────────────────────────────────────────
    def _on_button(self, text: str):
        t = text
        if t == "=":
            self._calculate()
        elif t == "AC":
            self._all_clear()
        elif t == "C":
            self._clear_last()
        elif t == "⌫":
            self._backspace()
        elif t == "±":
            self._negate()
        elif t == "MC":
            self.calc.memory_clear()
            self._update_mem_label()
        elif t == "MR":
            val = self.calc.memory_recall()
            self._append(str(val))
        elif t == "M+":
            self._mem_op("+")
        elif t == "M-":
            self._mem_op("-")
        elif t == "MS":
            try:
                v = float(self.display_var.get())
                self.calc.memory_store(v)
                self._update_mem_label()
            except ValueError:
                pass
        elif t == "ans":
            if self.calc.last_result is not None:
                self._append("ans")
        elif t == "π":
            self._append("pi")
        elif t == "e":
            self._append("e")
        elif t == "√":
            self._append("sqrt(")
        elif t == "x²":
            self._append("^2")
        elif t == "x³":
            self._append("^3")
        elif t == "xⁿ":
            self._append("^")
        elif t == "1/x":
            self._append("1/(")
        elif t == "fact":
            self._append("fact(")
        elif t in ("sin", "cos", "tan", "asin", "acos", "atan", "log", "ln"):
            self._append(t + "(")
        elif t == "÷":
            self._append("/")
        elif t == "×":
            self._append("*")
        elif t == "−":
            self._append("-")
        else:
            self._append(t)

    def _bind_keyboard(self):
        root = self.root
        root.bind("<Return>",     lambda e: self._calculate())
        root.bind("<KP_Enter>",   lambda e: self._calculate())
        root.bind("<BackSpace>",  lambda e: self._backspace())
        root.bind("<Delete>",     lambda e: self._all_clear())
        root.bind("<Escape>",     lambda e: self._all_clear())

        for ch in "0123456789.+-*/()%^":
            root.bind(ch, lambda e, c=ch: self._append(c))

    # ── Expression manipulation ───────────────────────────────────────────────
    def _append(self, text: str):
        if self.just_solved and text not in "+-*/^%)":
            # Start fresh after a result unless chaining with operator
            self.expression = ""
        self.just_solved = False
        self.expression += text
        self.expr_var.set(self.expression)
        self.display_var.set(self.expression or "0")

    def _calculate(self):
        if not self.expression:
            return
        result, ok = self.calc.calculate(self.expression)
        self.expr_var.set(self.expression + " =")
        self.display_var.set(result)
        if ok:
            self.expression   = result
            self.just_solved  = True
        else:
            self.expression = ""
        self._refresh_history()

    def _all_clear(self):
        self.expression = ""
        self.expr_var.set("")
        self.display_var.set("0")
        self.just_solved = False

    def _clear_last(self):
        # Remove last token (number or function name)
        import re
        expr = self.expression
        expr = re.sub(r'(sin|cos|tan|asin|acos|atan|sqrt|log|ln|fact|cbrt)\(?$|'
                      r'\d+\.?\d*$|[+\-*/^().%]$', '', expr)
        self.expression = expr
        self.expr_var.set(expr)
        self.display_var.set(expr or "0")

    def _backspace(self):
        if self.expression:
            self.expression = self.expression[:-1]
            self.expr_var.set(self.expression)
            self.display_var.set(self.expression or "0")

    def _negate(self):
        if self.expression:
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.expr_var.set(self.expression)
            self.display_var.set(self.expression)

    def _copy_result(self):
        val = self.display_var.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(val)

    def _mem_op(self, op: str):
        try:
            v = float(self.display_var.get())
            if op == "+":
                self.calc.memory_add(v)
            else:
                self.calc.memory_subtract(v)
            self._update_mem_label()
        except ValueError:
            pass

    def _update_mem_label(self):
        m = self.calc.memory.recall()
        self.mem_label.config(text=f"M = {m:.6g}" if m != 0 else "")

    # ── History ───────────────────────────────────────────────────────────────
    def _refresh_history(self):
        self.history_list.delete(0, "end")
        for entry in self.calc.history[:40]:
            self.history_list.insert("end", f"{entry.expression}")
            self.history_list.insert("end", f"  = {entry.result}")
            self.history_list.insert("end", f"  {entry.timestamp}")
            self.history_list.insert("end", "─" * 22)

    def _on_history_click(self, event):
        sel = self.history_list.curselection()
        if not sel:
            return
        line = self.history_list.get(sel[0])
        line = line.strip()
        if line.startswith("="):
            # paste the result value
            val = line[1:].strip()
            self._all_clear()
            self._append(val)
        elif not line.startswith("─") and not line[0].isdigit() or "=" not in line:
            # paste expression
            clean = line.strip()
            if clean and "─" not in clean:
                self._all_clear()
                self._append(clean)

    def _clear_history(self):
        if messagebox.askyesno("Clear History", "Delete all calculation history?"):
            self.calc.clear_history()
            self._refresh_history()

    # ── Solver dialog ─────────────────────────────────────────────────────────
    def _open_solver(self):
        SolverDialog(self.root, self.theme, self.calc)

    # ── Theme change ──────────────────────────────────────────────────────────
    def _on_theme_change(self, event):
        name = self.theme_var.get()
        self.theme = THEMES[name]
        # Rebuild UI with new theme
        for widget in self.root.winfo_children():
            widget.destroy()
        self._build_ui()
        self._refresh_history()
