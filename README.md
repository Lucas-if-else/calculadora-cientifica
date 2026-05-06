# Scientific Calculator — Python Desktop App

## Features
- Basic operations: + - * / % ^
- Scientific functions: sin, cos, tan, asin, acos, atan, log, ln, sqrt, exp, fact, abs, ceil, floor
- Constants: pi, e, tau
- Full expression support: `2*sin(30) + log(100)`
- Equation solver (linear & quadratic) via popup dialog
- Memory system: MC, MR, M+, M-, MS
- Calculation history (auto-saved, double-click to reuse)
- Copy result to clipboard
- Theme switcher: Cyberpunk / Neon Purple
- Keyboard input supported

## Project Structure

```
sci_calc/
├── main.py               ← Entry point
├── engine/
│   ├── __init__.py
│   ├── parser.py         ← Safe math parser (no eval!)
│   └── calculator.py     ← Engine: memory, history, solver
├── ui/
│   ├── __init__.py
│   ├── window.py         ← Tkinter GUI
│   └── theme.py          ← Color themes
└── data/
    └── history.json      ← Auto-created on first use
```

## Requirements

- Python 3.10+
- tkinter (usually bundled with Python)

### Install tkinter if missing:

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

**macOS (Homebrew):**
```bash
brew install python-tk
```

**Windows:** Tkinter is included with the official Python installer from python.org.

## How to Run

```bash
cd sci_calc
python main.py
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| 0–9, . | Input number |
| + - * / | Operators |
| ^ | Power |
| ( ) | Parentheses |
| Enter | Calculate |
| Backspace | Delete last char |
| Delete / Escape | All Clear |

## Extending the Calculator

To add a new math function:

1. Open `engine/parser.py`
2. Add to the `FUNCTIONS` dict:
   ```python
   "myFunc": lambda x: ...
   ```
3. Add a button in `ui/window.py` → `BUTTON_ROWS`

To add a new theme:

1. Open `ui/theme.py`
2. Create a new `Theme(...)` instance
3. Add it to the `THEMES` dict
