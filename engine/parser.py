"""
engine/parser.py
Safe mathematical expression parser using tokenization + recursive descent.
No eval() used - fully custom AST-based evaluation.
"""

import math
import re
from typing import Any


# ── Token types ──────────────────────────────────────────────────────────────
NUMBER   = "NUMBER"
IDENT    = "IDENT"
PLUS     = "PLUS"
MINUS    = "MINUS"
STAR     = "STAR"
SLASH    = "SLASH"
PERCENT  = "PERCENT"
CARET    = "CARET"
LPAREN   = "LPAREN"
RPAREN   = "RPAREN"
EOF      = "EOF"


class Token:
    def __init__(self, type_: str, value: Any):
        self.type  = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"


# ── Supported functions and constants ────────────────────────────────────────
FUNCTIONS = {
    "sin":   lambda x: math.sin(math.radians(x)),
    "cos":   lambda x: math.cos(math.radians(x)),
    "tan":   lambda x: math.tan(math.radians(x)),
    "asin":  lambda x: math.degrees(math.asin(x)),
    "acos":  lambda x: math.degrees(math.acos(x)),
    "atan":  lambda x: math.degrees(math.atan(x)),
    "sinh":  math.sinh,
    "cosh":  math.cosh,
    "tanh":  math.tanh,
    "log":   math.log10,
    "log2":  math.log2,
    "ln":    math.log,
    "sqrt":  math.sqrt,
    "cbrt":  lambda x: math.copysign(abs(x) ** (1/3), x),
    "abs":   abs,
    "ceil":  math.ceil,
    "floor": math.floor,
    "round": round,
    "exp":   math.exp,
    "fact":  lambda x: math.factorial(int(x)),
}

CONSTANTS = {
    "pi":  math.pi,
    "e":   math.e,
    "tau": math.tau,
    "inf": math.inf,
}


# ── Lexer ────────────────────────────────────────────────────────────────────
class Lexer:
    def __init__(self, text: str):
        self.text = text.strip()
        self.pos  = 0

    def error(self, msg: str = ""):
        raise SyntaxError(f"Invalid character at position {self.pos}" + (f": {msg}" if msg else ""))

    def peek(self):
        return self.text[self.pos] if self.pos < len(self.text) else None

    def advance(self):
        ch = self.text[self.pos]
        self.pos += 1
        return ch

    def skip_whitespace(self):
        while self.peek() and self.peek().isspace():
            self.advance()

    def read_number(self) -> Token:
        num_str = ""
        while self.peek() and (self.peek().isdigit() or self.peek() == "."):
            num_str += self.advance()
        # Scientific notation
        if self.peek() in ("e", "E"):
            num_str += self.advance()
            if self.peek() in ("+", "-"):
                num_str += self.advance()
            while self.peek() and self.peek().isdigit():
                num_str += self.advance()
        try:
            return Token(NUMBER, float(num_str))
        except ValueError:
            self.error(f"Malformed number: {num_str}")

    def read_ident(self) -> Token:
        ident = ""
        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            ident += self.advance()
        return Token(IDENT, ident)

    def tokenize(self) -> list[Token]:
        tokens = []
        while True:
            self.skip_whitespace()
            ch = self.peek()
            if ch is None:
                tokens.append(Token(EOF, None))
                break
            elif ch.isdigit() or ch == ".":
                tokens.append(self.read_number())
            elif ch.isalpha() or ch == "_":
                tokens.append(self.read_ident())
            elif ch == "+":  self.advance(); tokens.append(Token(PLUS,    "+"))
            elif ch == "-":  self.advance(); tokens.append(Token(MINUS,   "-"))
            elif ch == "*":  self.advance(); tokens.append(Token(STAR,    "*"))
            elif ch == "/":  self.advance(); tokens.append(Token(SLASH,   "/"))
            elif ch == "%":  self.advance(); tokens.append(Token(PERCENT, "%"))
            elif ch == "^":  self.advance(); tokens.append(Token(CARET,   "^"))
            elif ch == "(":  self.advance(); tokens.append(Token(LPAREN,  "("))
            elif ch == ")":  self.advance(); tokens.append(Token(RPAREN,  ")"))
            else:
                self.error(f"Unknown character '{ch}'")
        return tokens


# ── Recursive-descent parser / evaluator ─────────────────────────────────────
class Parser:
    """
    Grammar (in order of precedence, lowest first):
      expr     → term (('+' | '-') term)*
      term     → factor (('*' | '/' | '%') factor)*
      factor   → unary ('^' factor)?          (right-associative)
      unary    → ('-' | '+') unary | primary
      primary  → NUMBER | CONST | FUNC '(' expr ')' | '(' expr ')'
    """

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos    = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def consume(self, type_: str) -> Token:
        tok = self.tokens[self.pos]
        if tok.type != type_:
            raise SyntaxError(f"Expected {type_}, got {tok.type} ({tok.value!r})")
        self.pos += 1
        return tok

    def match(self, *types) -> bool:
        return self.peek().type in types

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    # ── Grammar rules ────────────────────────────────────────────────────────
    def parse(self) -> float:
        result = self.expr()
        if not self.match(EOF):
            raise SyntaxError("Unexpected token: " + str(self.peek().value))
        return result

    def expr(self) -> float:
        left = self.term()
        while self.match(PLUS, MINUS):
            op = self.advance().type
            right = self.term()
            left = left + right if op == PLUS else left - right
        return left

    def term(self) -> float:
        left = self.factor()
        while self.match(STAR, SLASH, PERCENT):
            op = self.advance().type
            right = self.factor()
            if op == STAR:
                left = left * right
            elif op == SLASH:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                left = left / right
            else:
                if right == 0:
                    raise ZeroDivisionError("Modulo by zero")
                left = left % right
        return left

    def factor(self) -> float:
        base = self.unary()
        if self.match(CARET):
            self.advance()
            exp = self.factor()       # right-associative
            return base ** exp
        return base

    def unary(self) -> float:
        if self.match(MINUS):
            self.advance()
            return -self.unary()
        if self.match(PLUS):
            self.advance()
            return self.unary()
        return self.primary()

    def primary(self) -> float:
        tok = self.peek()

        # Number literal
        if tok.type == NUMBER:
            self.advance()
            return tok.value

        # Identifier: constant or function
        if tok.type == IDENT:
            self.advance()
            name = tok.value.lower()

            # Constant
            if name in CONSTANTS:
                return CONSTANTS[name]

            # Function call
            if name in FUNCTIONS:
                self.consume(LPAREN)
                arg = self.expr()
                self.consume(RPAREN)
                try:
                    result = FUNCTIONS[name](arg)
                except (ValueError, OverflowError) as exc:
                    raise ValueError(f"{name}({arg}): {exc}")
                return result

            raise NameError(f"Unknown name: '{name}'")

        # Parenthesized expression
        if tok.type == LPAREN:
            self.advance()
            val = self.expr()
            self.consume(RPAREN)
            return val

        raise SyntaxError(f"Unexpected token: {tok.value!r}")


# ── Public API ───────────────────────────────────────────────────────────────
def evaluate(expression: str) -> float:
    """
    Parse and evaluate a math expression string safely.
    Returns a float result or raises an informative exception.
    """
    if not expression or not expression.strip():
        raise ValueError("Empty expression")

    # Normalize: replace implicit multiplication like 2sin → 2*sin
    expr = expression.strip()
    expr = re.sub(r"(\d)(sin|cos|tan|log|ln|sqrt|exp|abs|asin|acos|atan|fact|cbrt|ceil|floor|round|pi|e\b|tau)",
                  r"\1*\2", expr)
    expr = re.sub(r"\)\s*\(", r")*(", expr)   # )(  → )*(
    expr = re.sub(r"(\d)\s*\(", r"\1*(", expr) # 2(  → 2*(

    tokens = Lexer(expr).tokenize()
    return Parser(tokens).parse()
