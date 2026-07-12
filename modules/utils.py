"""
===========================================================
ZEXXPHISH
Advanced Phishing Analyzer

File: utils.py

Description:
Reusable utility functions used throughout the project.
===========================================================
"""

import os
import time
from modules.colors import Colors


def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")


def type_text(text, color=Colors.WHITE, delay=0.02):
    """
    Prints text with a typing animation.

    Parameters:
        text (str): Text to display.
        color (str): Text color.
        delay (float): Delay between characters.
    """
    print(color, end="")

    for character in text:
        print(character, end="", flush=True)
        time.sleep(delay)

    print(Colors.RESET)


def loading_screen():
    """
    Displays the startup loading sequence.
    """

    loading_messages = [
        ("[✓] Loading modules...", Colors.CYAN),
        ("[✓] Initializing scanner...", Colors.CYAN),
        ("[✓] Loading threat signatures...", Colors.CYAN),
        ("[✓] Ready.", Colors.GREEN)
    ]

    for message, color in loading_messages:
        type_text(message, color, 0.015)
        time.sleep(0.20)

    print()