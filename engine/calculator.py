"""
engine/calculator.py
Core calculator logic: memory system, history, equation solver.
Pure logic – no GUI dependencies.
"""

import math
import json
import os
from datetime import datetime
from typing import Optional
from .parser import evaluate


HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "history.json")


class Memory:
    """M+, M-, MR, MC memory bank."""

    def __init__(self):
        self._value: float = 0.0

    def store(self, value: float):
        """MC then store (MS)."""
        self._value = value

    def add(self, value: float):
        """M+"""
        self._value += value

    def subtract(self, value: float):
        """M-"""
        self._value -= value

    def recall(self) -> float:
        """MR"""
        return self._value

    def clear(self):
        """MC"""
        self._value = 0.0

    @property
    def has_value(self) -> bool:
        return self._value != 0.0


class HistoryEntry:
    def __init__(self, expression: str, result: str, timestamp: str = ""):
        self.expression = expression
        self.result     = result
        self.timestamp  = timestamp or datetime.now().strftime("%H:%M:%S")

    def to_dict(self):
        return {"expression": self.expression,
                "result":     self.result,
                "timestamp":  self.timestamp}

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d["expression"], d["result"], d.get("timestamp", ""))


class Calculator:
    """
    Main calculator engine.
    Handles evaluation, memory, history, and equation solving.
    """

    def __init__(self):
        self.memory       = Memory()
        self.history: list[HistoryEntry] = []
        self.last_result: Optional[float] = None
        self._load_history()

    # ── Evaluation ───────────────────────────────────────────────────────────
    def calculate(self, expression: str) -> tuple[str, bool]:
        """
        Evaluate expression.
        Returns (result_str, success: bool).
        Adds to history on success.
        """
        try:
            # Allow 'ans' to refer to last result
            expr = expression
            if self.last_result is not None:
                expr = expr.replace("ans", str(self.last_result))

            result = evaluate(expr)

            # Format result
            if isinstance(result, float):
                if result == int(result) and abs(result) < 1e15:
                    result_str = str(int(result))
                else:
                    result_str = f"{result:.10g}"
            else:
                result_str = str(result)

            self.last_result = result
            entry = HistoryEntry(expression, result_str)
            self.history.insert(0, entry)
            if len(self.history) > 100:
                self.history = self.history[:100]
            self._save_history()
            return result_str, True

        except ZeroDivisionError:
            return "Error: Division by zero", False
        except (SyntaxError, ValueError, NameError, OverflowError) as exc:
            return f"Error: {exc}", False
        except Exception as exc:
            return f"Error: {exc}", False

    # ── Equation solver ──────────────────────────────────────────────────────
    def solve_linear(self, a: float, b: float) -> str:
        """Solve ax + b = 0  →  x = -b/a"""
        if a == 0:
            if b == 0:
                return "Infinite solutions (0 = 0)"
            return "No solution (contradiction)"
        x = -b / a
        return f"x = {x:.10g}"

    def solve_quadratic(self, a: float, b: float, c: float) -> str:
        """Solve ax² + bx + c = 0"""
        if a == 0:
            return self.solve_linear(b, c)
        disc = b**2 - 4*a*c
        if disc > 0:
            x1 = (-b + math.sqrt(disc)) / (2*a)
            x2 = (-b - math.sqrt(disc)) / (2*a)
            return f"x₁ = {x1:.10g},  x₂ = {x2:.10g}"
        elif disc == 0:
            x = -b / (2*a)
            return f"x = {x:.10g}  (double root)"
        else:
            real = -b / (2*a)
            imag = math.sqrt(-disc) / (2*a)
            sign = "+" if imag >= 0 else "-"
            return f"x₁ = {real:.6g} + {abs(imag):.6g}i,  x₂ = {real:.6g} - {abs(imag):.6g}i"

    # ── Memory wrappers ──────────────────────────────────────────────────────
    def memory_add(self, value: float):       self.memory.add(value)
    def memory_subtract(self, value: float):  self.memory.subtract(value)
    def memory_recall(self) -> float:         return self.memory.recall()
    def memory_clear(self):                   self.memory.clear()
    def memory_store(self, value: float):     self.memory.store(value)

    # ── History persistence ──────────────────────────────────────────────────
    def clear_history(self):
        self.history.clear()
        self._save_history()

    def _save_history(self):
        try:
            os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
            with open(HISTORY_FILE, "w") as f:
                json.dump([e.to_dict() for e in self.history], f, indent=2)
        except OSError:
            pass

    def _load_history(self):
        try:
            with open(HISTORY_FILE) as f:
                data = json.load(f)
                self.history = [HistoryEntry.from_dict(d) for d in data]
        except (OSError, json.JSONDecodeError):
            self.history = []
