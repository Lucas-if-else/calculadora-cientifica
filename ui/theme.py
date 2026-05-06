"""
ui/theme.py
Color themes for the calculator.
All colors are standard Tk color strings.
"""

from dataclasses import dataclass


@dataclass
class Theme:
    name: str
    # Backgrounds
    bg_main:     str
    bg_display:  str
    bg_sidebar:  str
    bg_btn:      str
    bg_btn_op:   str   # operator buttons
    bg_btn_fn:   str   # function buttons
    bg_btn_eq:   str   # equals button
    bg_btn_mem:  str   # memory buttons
    bg_btn_spec: str   # C / AC
    # Foregrounds
    fg_main:     str
    fg_display:  str
    fg_expr:     str
    fg_btn:      str
    fg_btn_eq:   str
    fg_sidebar:  str
    fg_history:  str
    # Accents
    accent:      str
    accent2:     str
    # Hover deltas (lighter shade for the same btn bg)
    hover_btn:   str
    hover_op:    str
    hover_eq:    str


CYBERPUNK = Theme(
    name        = "Cyberpunk",
    bg_main     = "#0d0d0d",
    bg_display  = "#111118",
    bg_sidebar  = "#0a0a12",
    bg_btn      = "#1a1a2e",
    bg_btn_op   = "#16213e",
    bg_btn_fn   = "#0f1535",
    bg_btn_eq   = "#00d4aa",
    bg_btn_mem  = "#1a0f35",
    bg_btn_spec = "#2d0a0a",
    fg_main     = "#e0e0f0",
    fg_display  = "#00ffcc",
    fg_expr     = "#7070a0",
    fg_btn      = "#c0c0e0",
    fg_btn_eq   = "#000000",
    fg_sidebar  = "#e0e0f0",
    fg_history  = "#8080b0",
    accent      = "#00ffcc",
    accent2     = "#ff00aa",
    hover_btn   = "#252545",
    hover_op    = "#1e2d55",
    hover_eq    = "#00b890",
)

NEON_PURPLE = Theme(
    name        = "Neon Purple",
    bg_main     = "#0e0010",
    bg_display  = "#130018",
    bg_sidebar  = "#0a000e",
    bg_btn      = "#1c0030",
    bg_btn_op   = "#200038",
    bg_btn_fn   = "#180028",
    bg_btn_eq   = "#cc00ff",
    bg_btn_mem  = "#250040",
    bg_btn_spec = "#300010",
    fg_main     = "#e8d0ff",
    fg_display  = "#dd88ff",
    fg_expr     = "#885588",
    fg_btn      = "#cc99ff",
    fg_btn_eq   = "#ffffff",
    fg_sidebar  = "#e8d0ff",
    fg_history  = "#885599",
    accent      = "#cc00ff",
    accent2     = "#ff6600",
    hover_btn   = "#2a0045",
    hover_op    = "#2e0050",
    hover_eq    = "#aa00dd",
)

THEMES = {
    "Cyberpunk":    CYBERPUNK,
    "Neon Purple":  NEON_PURPLE,
}
