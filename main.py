"""
main.py
Entry point for the Scientific Calculator application.
Run with: python main.py
"""

import sys
import os

# Ensure the project root is in the Python path
sys.path.insert(0, os.path.dirname(__file__))

from ui.window import MainWindow


def main():
    app = MainWindow()


if __name__ == "__main__":
    main()
